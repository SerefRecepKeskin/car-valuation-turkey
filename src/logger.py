"""
Simple colored logger for clean terminal output.
"""


class Logger:
    """Formatted terminal output with ANSI colors."""

    # ANSI escape codes
    _R = "\033[0m"       # Reset
    _B = "\033[1m"       # Bold
    _D = "\033[2m"       # Dim
    _RED = "\033[91m"
    _GRN = "\033[92m"
    _YLW = "\033[93m"
    _BLU = "\033[94m"
    _MAG = "\033[95m"
    _CYN = "\033[96m"

    def header(self, title, subtitle=""):
        """Print a prominent header block."""
        line = "=" * 60
        print(f"\n{self._CYN}{line}{self._R}")
        print(f"  {self._B}{title}{self._R}")
        if subtitle:
            print(f"  {self._D}{subtitle}{self._R}")
        print(f"{self._CYN}{line}{self._R}")

    def section(self, title):
        """Print a section divider."""
        line = "-" * 60
        print(f"\n{self._CYN}{line}{self._R}")
        print(f"  {self._B}{title}{self._R}")
        print(f"{self._CYN}{line}{self._R}")

    def step(self, current, total, msg):
        """Print a pipeline step indicator."""
        print(f"\n{self._MAG}[{current}/{total}]{self._R} {self._B}{msg}{self._R}")

    def info(self, msg):
        """Print an info message."""
        print(f"  {self._BLU}>{self._R} {msg}")

    def success(self, msg):
        """Print a success message."""
        print(f"  {self._GRN}>{self._R} {msg}")

    def warning(self, msg):
        """Print a warning message."""
        print(f"  {self._YLW}>{self._R} {msg}")

    def error(self, msg):
        """Print an error message."""
        print(f"  {self._RED}>{self._R} {msg}")

    def metric(self, label, value):
        """Print a label-value pair."""
        print(f"  {self._D}{label:<28s}{self._R}: {value}")

    def result(self, msg):
        """Print a highlighted result."""
        print(f"\n  {self._GRN}{self._B}{msg}{self._R}")

    def table(self, headers, rows):
        """Print a formatted table."""
        widths = []
        for i in range(len(headers)):
            max_w = len(str(headers[i]))
            for row in rows:
                max_w = max(max_w, len(str(row[i])))
            widths.append(max_w + 1)

        header_str = " | ".join(
            f"{self._B}{str(h):<{w}}{self._R}" for h, w in zip(headers, widths)
        )
        sep_str = "-+-".join("-" * w for w in widths)
        print(f"\n  {header_str}")
        print(f"  {sep_str}")
        for row in rows:
            row_str = " | ".join(f"{str(v):<{w}}" for v, w in zip(row, widths))
            print(f"  {row_str}")

    def blank(self):
        print()


log = Logger()
