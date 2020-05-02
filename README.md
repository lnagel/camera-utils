# camera-utils

## portrait_mover.py

Moves files from the Google Camera portrait-style folders into regular .jpg files if only one image remains in the portrait folder.

Example:

```
$ python portrait_mover.py Camera/
INFO:portrait_mover:MV Camera/{IMG_20200329_125701/00100lrPORTRAIT_00100_BURST20200329125701697_COVER.jpg -> IMG_20200329_125701.jpg}
INFO:portrait_mover:MV Camera/{IMG_20200329_125737/00000PORTRAIT_00000_BURST20200329125737968.jpg -> IMG_20200329_125737.jpg}
INFO:portrait_mover:MV Camera/{IMG_20200329_125710/00100lrPORTRAIT_00100_BURST20200329125710133_COVER.jpg -> IMG_20200329_125710.jpg}
INFO:portrait_mover:MV Camera/{IMG_20200329_125718/00100lrPORTRAIT_00100_BURST20200329125718402_COVER.jpg -> IMG_20200329_125718.jpg}
```
