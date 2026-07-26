# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""Entry point: python3 -m notarius <check|seal|verify> (AD-64)."""

from notarius.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
