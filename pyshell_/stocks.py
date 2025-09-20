import yfinance as yf
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime


class Stock:
    def get_stock_info(self, args):
        console = Console()
        if not args:
            console.print("Usage: stock <symbol>", style="bold red")
            console.print("Example: stock AAPL", style="bold yellow")
            return

        symbol = args[0].upper()

        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            hist = ticker.history(period="1d")

            if hist.empty or not info:
                console.print(
                    f"Error: No data found for symbol {symbol}", style="bold red"
                )
                return

            current_price = hist["Close"].iloc[-1]
            prev_close = info.get("previousClose", 0)
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100 if prev_close != 0 else 0

            change_color = "green" if change >= 0 else "red"
            change_symbol = "▲" if change >= 0 else "▼"

            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_column("Field", style="bold cyan", width=20)
            table.add_column("Value", style="white")

            table.add_row("📈 Symbol:", f"[bold]{info.get('symbol', symbol)}[/bold]")
            table.add_row("🏢 Company:", info.get("longName", "N/A"))
            table.add_row("💰 Current Price:", f"${current_price:.2f}")
            table.add_row(
                "📊 Change:",
                f"[{change_color}]{change_symbol} ${change:.2f} ({change_percent:+.2f}%)[/{change_color}]",
            )
            table.add_row("🔄 Previous Close:", f"${prev_close:.2f}")

            if "dayHigh" in info and "dayLow" in info:
                table.add_row("📈 Day High:", f"${info['dayHigh']:.2f}")
                table.add_row("📉 Day Low:", f"${info['dayLow']:.2f}")

            if "volume" in info:
                volume = info["volume"]
                if volume >= 1_000_000:
                    volume_str = f"{volume / 1_000_000:.1f}M"
                elif volume >= 1_000:
                    volume_str = f"{volume / 1_000:.1f}K"
                else:
                    volume_str = str(volume)
                table.add_row("📦 Volume:", volume_str)

            if "marketCap" in info and info["marketCap"]:
                market_cap = info["marketCap"]
                if market_cap >= 1_000_000_000_000:
                    cap_str = f"${market_cap / 1_000_000_000_000:.2f}T"
                elif market_cap >= 1_000_000_000:
                    cap_str = f"${market_cap / 1_000_000_000:.2f}B"
                elif market_cap >= 1_000_000:
                    cap_str = f"${market_cap / 1_000_000:.2f}M"
                else:
                    cap_str = f"${market_cap:,.0f}"
                table.add_row("🏦 Market Cap:", cap_str)

            if "fiftyTwoWeekHigh" in info and "fiftyTwoWeekLow" in info:
                table.add_row("📅 52W High:", f"${info['fiftyTwoWeekHigh']:.2f}")
                table.add_row("📅 52W Low:", f"${info['fiftyTwoWeekLow']:.2f}")

            if "dividendYield" in info and info["dividendYield"]:
                dividend_yield = info["dividendYield"] * 100
                table.add_row("💎 Dividend Yield:", f"{dividend_yield:.2f}%")

            if "trailingPE" in info and info["trailingPE"]:
                table.add_row("📊 P/E Ratio:", f"{info['trailingPE']:.2f}")

            panel_title = f"📊 Stock Information - {symbol}"
            panel = Panel(table, title=panel_title, border_style="cyan")

            console.print()
            console.print(panel)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            console.print(f"\n[dim]Last updated: {timestamp}[/dim]", justify="right")

        except Exception as e:
            console.print(f"Failed to fetch stock data: {str(e)}", style="bold red")
            console.print(
                "Please check if the symbol is correct and try again.", style="yellow"
            )

    def get_multiple_stocks(self, args):
        """Get information for multiple stocks"""
        console = Console()
        if not args:
            console.print("Usage: stocks <symbol1> <symbol2> ...", style="bold red")
            console.print("Example: stocks AAPL GOOGL MSFT", style="bold yellow")
            return

        symbols = [symbol.upper() for symbol in args]

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Symbol", style="bold white", width=10)
        table.add_column("Company", style="white", width=25)
        table.add_column("Price", style="white", width=12)
        table.add_column("Change", style="white", width=15)
        table.add_column("Volume", style="white", width=12)

        try:
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period="1d")

                if hist.empty or not info:
                    table.add_row(symbol, "N/A", "N/A", "N/A", "N/A")
                    continue

                current_price = hist["Close"].iloc[-1]
                prev_close = info.get("previousClose", 0)
                change = current_price - prev_close
                change_percent = (change / prev_close) * 100 if prev_close != 0 else 0

                change_color = "green" if change >= 0 else "red"
                change_symbol = "▲" if change >= 0 else "▼"

                company_name = info.get("longName", "N/A")
                if len(company_name) > 22:
                    company_name = company_name[:22] + "..."

                volume = info.get("volume", 0)
                if volume >= 1_000_000:
                    volume_str = f"{volume / 1_000_000:.1f}M"
                elif volume >= 1_000:
                    volume_str = f"{volume / 1_000:.1f}K"
                else:
                    volume_str = str(volume)

                table.add_row(
                    symbol,
                    company_name,
                    f"${current_price:.2f}",
                    f"[{change_color}]{change_symbol} {change_percent:+.2f}%[/{change_color}]",
                    volume_str,
                )

            panel = Panel(table, title="📊 Stock Comparison", border_style="cyan")
            console.print()
            console.print(panel)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            console.print(f"\n[dim]Last updated: {timestamp}[/dim]", justify="right")

        except Exception as e:
            console.print(f"Failed to fetch stock data: {str(e)}", style="bold red")


if __name__ == "__main__":
    Stock().get_stock_info(["MSFT"])
    Stock().get_multiple_stocks(["MSFT", "AAPL", "GOOGL"])
