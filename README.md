# Raydium Scalper Bot

A professional Solana trading bot that automatically scans and trades trending tokens on Raydium DEX using the SpiderSwap API.

## Features

- 🔍 Real-time trending token scanning
- 💹 Automated trading based on market analysis
- 📊 Professional TUI (Text User Interface)
- 🔒 Secure configuration management
- 📈 Profit tracking and performance monitoring
- ⚡ Fast execution using SpiderSwap API

## Prerequisites

- Python 3.8 or higher
- Solana wallet with SOL for trading
- SpiderSwap API key
- Helius RPC URL (or other Solana RPC provider)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Raydium_Scalper.git
cd Raydium_Scalper
```

2. Run the start script:
```bash
start.bat
```

This will:
- Create a virtual environment
- Install required dependencies
- Create a `.env` file template
- Launch the bot interface

3. Configure your `.env` file with your credentials:
```
PRIVATE_KEY=your_solana_wallet_private_key
RPC_URL=your_helius_rpc_url
SPIDER_SWAP_URL=https://api.spiderswap.com/v1/swap
SPIDER_SWAP_API_KEY=your_spider_swap_api_key
SOL_ADDRESS=So11111111111111111111111111111111111111112
```

## Usage

1. Launch the bot:
```bash
start.bat
```

2. Use the interactive menu:
   - `1`: Configure Bot - Set up your credentials
   - `2`: Show Configuration - View current settings
   - `3`: Scan Trending Tokens - View current market opportunities
   - `4`: Start Trading Bot - Begin automated trading
   - `5`: Show Bot Status - Monitor bot performance
   - `6`: Exit - Safely close the bot

## Trading Strategy

The bot uses a sophisticated strategy to identify and trade trending tokens:

1. **Token Scanning**:
   - Monitors trending pools on Raydium
   - Analyzes volume, liquidity, and price changes
   - Calculates buy/sell ratios
   - Scores tokens based on multiple metrics

2. **Entry Criteria**:
   - Market cap between $500K and $40M
   - Positive price momentum
   - High trading volume
   - Favorable buy/sell ratio

3. **Exit Strategy**:
   - 15% profit target
   - 20-minute maximum hold time
   - Dynamic slippage adjustment
   - Multiple retry attempts for reliable execution

## Safety Features

- Configuration validation before trading
- Secure credential management
- Transaction verification
- Error handling and recovery
- Safe exit procedures

## Dependencies

- aiohttp: Async HTTP client
- python-dotenv: Environment variable management
- requests: HTTP requests
- solders: Solana blockchain interaction
- click: CLI interface
- rich: Terminal UI components

## Logging

The bot maintains detailed logs in `scanner.log` for:
- Token scanning results
- Trading decisions
- Transaction status
- Error messages
- Performance metrics

## Disclaimer

This bot is for educational purposes only. Trading cryptocurrencies carries significant risks. Always:
- Start with small amounts
- Monitor the bot's performance
- Keep your private keys secure
- Understand the trading strategy
- Be aware of market risks

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please open an issue on the GitHub repository. 