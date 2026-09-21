# HTML Object Scene Schema

`extract-html-objects.mjs` writes a compact scene graph consumed by `create-object-html-pptx.mjs`.

```json
{
  "width": 1280,
  "height": 720,
  "slides": [
    {
      "slide": 1,
      "background": "#ffffff",
      "elements": [
        {
          "kind": "text",
          "order": 0,
          "zIndex": 0,
          "position": {"left": 48, "top": 72, "width": 520, "height": 80},
          "text": "Editable headline",
          "style": {"fontSize": 38, "bold": true, "color": "#070154"}
        },
        {
          "kind": "shape",
          "shape": "rect",
          "order": 1,
          "zIndex": 0,
          "position": {"left": 50, "top": 212, "width": 576, "height": 386},
          "fill": "#e8eef8"
        },
        {
          "kind": "image",
          "order": 2,
          "zIndex": 1,
          "position": {"left": 723, "top": 125, "width": 557, "height": 557},
          "src": "https://assets.example.com/photo.jpeg",
          "fit": "cover"
        }
      ]
    }
  ]
}
```

Validation targets:

- one scene slide per HTML `section.slide`
- no single image at `0,0,1280,720` unless explicitly requested
- text content appears as `kind: "text"`
- background fills appear as `kind: "shape"`
- image tags and CSS background URLs appear as `kind: "image"`
- `order` preserves DOM order and `zIndex` records explicit stacking intent
- scene width and height match the authored slide canvas when it can be measured
