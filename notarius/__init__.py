# SPDX-License-Identifier: LicenseRef-Proprietary
# SPDX-FileCopyrightText: 2026 Ruslan Malyavskiy
"""NOTARIUS — semantic provenance tracing for a data element.

Author: Ruslan Malyavskiy. License: PROPRIETARY — all rights reserved (AD-82,
see LICENSE). The repository is view-only; use is by written permission.
Parent framework: E-Continuity / governed recoverability.

The core is semantic tracing (docs/SEMANTIC_TRACE_CANON): where an element
came from, what it passed through, whether it is native or spliced in.
Signing / threshold / witnesses / recovery are plumbing in service of the trace.

Modules are installed on demand; the heavy ones (integrations — reedsolo /
opentimestamps) are NOT imported here, so the package works without optional
dependencies. Import narrowly: `from notarius.trace import verify_trace`.
"""

__version__ = "0.1.0"
__author__ = "Ruslan Malyavskiy"
