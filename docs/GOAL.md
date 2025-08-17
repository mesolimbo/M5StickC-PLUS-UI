This pipenv project aims to produce a graphical user interface for the M5StickC-PLUS.

Two hardware/design specs are provided in docs/SPECS-A.md and docs/SPECS-B.md.

The library is expected to read and display BMP images on device.

The library is expected to draw lines, geometric shapes, and text.

Any graphic displayed on the screen must appear immediately, that is using a framebuffer or double buffering. We do not want to see a flicker, pixel-by-pixel rendering, or any other kind of partial rendering.

We want to minimize the number of external dependencies.