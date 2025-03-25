import click
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from dotenv import load_dotenv, set_key
import asyncio
from trend import TokenScanner
from swap import TradingBot, TradeAction
from datetime import datetime

console = Console()

def load_config():
    """Load configuration from .env file"""
    load_dotenv()
    return {
        'private_key': os.getenv('PRIVATE_KEY'),
        'rpc_url': os.getenv('RPC_URL'),
        'spider_swap_url': os.getenv('SPIDER_SWAP_URL'),
        'spider_swap_api_key': os.getenv('SPIDER_SWAP_API_KEY'),
        'sol_address': os.getenv('SOL_ADDRESS')
    }

def save_config(config):
    """Save configuration to .env file"""
    for key, value in config.items():
        set_key('.env', key.upper(), value)

def display_config(config):
    """Display current configuration in a formatted table"""
    table = Table(title="Current Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in config.items():
        # Mask sensitive information
        if key in ['private_key', 'spider_swap_api_key']:
            value = '********' + value[-4:] if value else 'Not Set'
        table.add_row(key.replace('_', ' ').title(), str(value))
    
    return table

@click.group()
def cli():
    """Raydium Scalper - Solana Trading Bot"""
    pass

@cli.command()
def configure():
    """Configure the trading bot settings"""
    config = load_config()
    
    console.print(Panel.fit(
        "[bold yellow]Raydium Scalper Configuration[/bold yellow]\n"
        "Please enter your configuration details below.\n"
        "Press Enter to keep the current value.",
        title="Configuration Wizard"
    ))
    
    # Get RPC URL
    rpc_url = Prompt.ask(
        "Solana RPC URL",
        default=config['rpc_url'] or "https://mainnet.helius-rpc.com/?api-key=YOUR-API-KEY"
    )
    
    # Get SpiderSwap API Key
    spider_swap_api_key = Prompt.ask(
        "SpiderSwap API Key",
        default=config['spider_swap_api_key'] or "YOUR-API-KEY"
    )
    
    # Get SpiderSwap URL
    spider_swap_url = Prompt.ask(
        "SpiderSwap API URL",
        default=config['spider_swap_url'] or "https://api.spiderswap.com/v1/swap"
    )
    
    # Get Private Key
    private_key = Prompt.ask(
        "Solana Wallet Private Key (base58)",
        default=config['private_key'] or "YOUR-PRIVATE-KEY"
    )
    
    # Update config
    config.update({
        'rpc_url': rpc_url,
        'spider_swap_api_key': spider_swap_api_key,
        'spider_swap_url': spider_swap_url,
        'private_key': private_key,
        'sol_address': config['sol_address'] or "So11111111111111111111111111111111111111112"
    })
    
    # Save configuration
    save_config(config)
    console.print("[green]Configuration saved successfully![/green]")

@cli.command()
def show_config():
    """Display current configuration"""
    config = load_config()
    console.print(display_config(config))

@cli.command()
def scan_tokens():
    """Scan for trending tokens"""
    config = load_config()
    if not all([config['rpc_url'], config['spider_swap_api_key']]):
        console.print("[red]Error: Please configure the bot first using 'configure' command[/red]")
        return
    
    console.print(Panel.fit(
        "[bold yellow]Scanning for Trending Tokens[/bold yellow]\n"
        "This will show you the top trending tokens on Solana.",
        title="Token Scanner"
    ))
    
    scanner = TokenScanner()
    asyncio.run(scanner.get_trending_tokens())

@cli.command()
def start_bot():
    """Start the trading bot"""
    config = load_config()
    if not all(config.values()):
        console.print("[red]Error: Please configure the bot first using 'configure' command[/red]")
        return
    
    console.print(Panel.fit(
        "[bold yellow]Starting Raydium Scalper Bot[/bold yellow]\n"
        "The bot will now monitor for trading opportunities.",
        title="Trading Bot"
    ))
    
    bot = TradingBot(
        private_key=config['private_key'],
        rpc_url=config['rpc_url'],
        swap_url=config['spider_swap_url'],
        api_key=config['spider_swap_api_key'],
        sol_mint=config['sol_address']
    )
    
    scanner = TokenScanner()
    asyncio.run(listen_for_events(bot, scanner))

@cli.command()
def status():
    """Show bot status and statistics"""
    config = load_config()
    if not all(config.values()):
        console.print("[red]Error: Please configure the bot first using 'configure' command[/red]")
        return
    
    console.print(Panel.fit(
        "[bold yellow]Bot Status[/bold yellow]\n"
        "Displaying current bot status and statistics.",
        title="Status"
    ))
    
    # Here you would implement status checking logic
    # For now, we'll just show a placeholder
    table = Table(title="Bot Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Trades Executed", "0")
    table.add_row("Total Profit", "$0.00")
    table.add_row("Current Position", "None")
    table.add_row("Uptime", "Not Started")
    
    console.print(table)

def configure_bot():
    """Interactive configuration wizard"""
    config = load_config()
    
    console.print(Panel.fit(
        "[bold yellow]Raydium Scalper Configuration[/bold yellow]\n"
        "Please enter your configuration details below.\n"
        "Press Enter to keep the current value.",
        title="Configuration Wizard"
    ))
    
    # Get RPC URL
    rpc_url = Prompt.ask(
        "Solana RPC URL",
        default=config['rpc_url'] or "https://mainnet.helius-rpc.com/?api-key=YOUR-API-KEY"
    )
    
    # Get SpiderSwap API Key
    spider_swap_api_key = Prompt.ask(
        "SpiderSwap API Key",
        default=config['spider_swap_api_key'] or "YOUR-API-KEY"
    )
    
    # Get SpiderSwap URL
    spider_swap_url = Prompt.ask(
        "SpiderSwap API URL",
        default=config['spider_swap_url'] or "https://api.spiderswap.com/v1/swap"
    )
    
    # Get Private Key
    private_key = Prompt.ask(
        "Solana Wallet Private Key (base58)",
        default=config['private_key'] or "YOUR-PRIVATE-KEY"
    )
    
    # Update config
    config.update({
        'rpc_url': rpc_url,
        'spider_swap_api_key': spider_swap_api_key,
        'spider_swap_url': spider_swap_url,
        'private_key': private_key,
        'sol_address': config['sol_address'] or "So11111111111111111111111111111111111111112"
    })
    
    # Save configuration
    save_config(config)
    console.print("[green]Configuration saved successfully![/green]")
    return config

def get_bot_status():
    """Get current bot status"""
    config = load_config()
    if not all(config.values()):
        return "Not Configured"
    return "Ready to Start"

def validate_config():
    """Validate current configuration"""
    config = load_config()
    missing = [key for key, value in config.items() if not value]
    if missing:
        return False, f"Missing configuration: {', '.join(missing)}"
    return True, "Configuration valid"

if __name__ == '__main__':
    cli() 