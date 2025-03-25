import os
import sys
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from datetime import datetime
import time
from cli import (
    load_config, save_config, display_config, configure_bot,
    get_bot_status, validate_config
)
from trend import TokenScanner
from swap import TradingBot, TradeAction

console = Console()

def create_header():
    """Create the header panel"""
    return Panel(
        "[bold blue]Raydium Scalper Bot[/bold blue]\n"
        "[yellow]Professional Solana Trading Bot[/yellow]",
        style="bold white",
        expand=False
    )

def create_menu():
    """Create the main menu table"""
    table = Table(show_header=False, box=None, expand=False)
    table.add_row("[bold cyan]1[/bold cyan]", "Configure Bot")
    table.add_row("[bold cyan]2[/bold cyan]", "Show Configuration")
    table.add_row("[bold cyan]3[/bold cyan]", "Scan Trending Tokens")
    table.add_row("[bold cyan]4[/bold cyan]", "Start Trading Bot")
    table.add_row("[bold cyan]5[/bold cyan]", "Show Bot Status")
    table.add_row("[bold cyan]6[/bold cyan]", "Exit")
    return Panel(table, title="Menu", border_style="blue", expand=False)

def create_status_panel(status_text="Ready to start"):
    """Create the status panel"""
    return Panel(
        f"[bold green]Bot Status[/bold green]\n{status_text}",
        title="Status",
        border_style="green",
        expand=False
    )

def create_log_panel(log_text="No recent activity"):
    """Create the log panel"""
    return Panel(
        f"[bold yellow]Bot Log[/bold yellow]\n{log_text}",
        title="Log",
        border_style="yellow",
        expand=False
    )

async def scan_tokens():
    """Scan for trending tokens"""
    scanner = TokenScanner()
    tokens = await scanner.get_trending_tokens()
    
    table = Table(title="Trending Tokens", expand=True)
    table.add_column("Name", style="cyan")
    table.add_column("Address", style="green")
    table.add_column("Price", style="yellow")
    table.add_column("Volume 1h", style="magenta")
    table.add_column("Price Change", style="red")
    
    for token in tokens[:5]:  # Show top 5 tokens
        table.add_row(
            token['name'],
            token['address'][:8] + "...",
            f"${token['base_token_price']:.8f}",
            f"${token['volume_1h']:,.2f}",
            f"{token['price_change_1h']}%"
        )
    
    return table

async def start_bot():
    """Start the trading bot"""
    # Validate configuration
    is_valid, message = validate_config()
    if not is_valid:
        return f"Error: {message}"
    
    config = load_config()
    try:
        bot = TradingBot(
            private_key=config['private_key'],
            rpc_url=config['rpc_url'],
            swap_url=config['spider_swap_url'],
            api_key=config['spider_swap_api_key'],
            sol_mint=config['sol_address']
        )
        scanner = TokenScanner()
        return "Bot started successfully"
    except Exception as e:
        return f"Error starting bot: {str(e)}"

def main():
    """Main menu loop"""
    # Create the layout
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main")
    )
    
    # Split the main area into menu and content
    layout["main"].split_row(
        Layout(name="menu", ratio=1),
        Layout(name="content", ratio=2)
    )
    
    # Split the content area into status and log
    layout["content"].split(
        Layout(name="status", ratio=1),
        Layout(name="log", ratio=1)
    )
    
    bot_running = False
    log_messages = []
    
    while True:
        # Clear screen
        console.clear()
        
        # Update layout
        layout["header"].update(create_header())
        layout["menu"].update(create_menu())
        layout["status"].update(create_status_panel(get_bot_status()))
        layout["log"].update(create_log_panel("\n".join(log_messages[-5:])))
        
        # Display the layout
        console.print(layout)
        
        # Get user input
        choice = Prompt.ask("\nEnter your choice", choices=["1", "2", "3", "4", "5", "6"])
        
        if choice == "1":
            # Configure bot
            configure_bot()
            log_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] Configuration updated")
            
        elif choice == "2":
            # Show configuration
            config = load_config()
            console.print(display_config(config))
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            # Scan tokens
            console.print("\nScanning for trending tokens...")
            tokens_table = asyncio.run(scan_tokens())
            console.print(tokens_table)
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            # Start bot
            if not bot_running:
                status = asyncio.run(start_bot())
                if "Error" not in status:
                    bot_running = True
                log_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] {status}")
            else:
                log_messages.append(f"[{datetime.now().strftime('%H:%M:%S')}] Bot is already running")
            
        elif choice == "5":
            # Show status
            status_text = "Bot is running" if bot_running else "Bot is stopped"
            layout["status"].update(create_status_panel(status_text))
            input("\nPress Enter to continue...")
            
        elif choice == "6":
            # Exit
            if bot_running:
                if Confirm.ask("Bot is running. Are you sure you want to exit?"):
                    break
            else:
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Bot stopped by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
    finally:
        console.print("\n[green]Thank you for using Raydium Scalper Bot![/green]") 