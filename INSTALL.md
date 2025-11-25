# Series Page v5 - Complete Installation Guide

## What's New in v5

### Smart Tab Display for Standalone Series

**Problem:** Standalone graphic novels, one-shots, and TPBs were hidden in the Specials tab, leaving the Issues tab empty.

**Solution:** If a series has NO plain issues, everything is promoted to the Issues tab. Annuals and Specials tabs are auto-hidden.

## Quick Examples

### Before v5 (Broken UX)
```
"Batman: The Killing Joke" (1 Graphic Novel)
Tabs: [Volumes] [Issues ✗ EMPTY] [Specials ✓ Has it]
      User confused, has to hunt for content
```

### After v5 (Good UX)
```
"Batman: The Killing Joke" (1 Graphic Novel)
Tabs: [Volumes] [Issues ✓ Shows it with badge] [Related] [Details]
      Annuals and Specials tabs hidden (not needed)
```

## Installation

### Step 1: Update API (if not done in v4)
```bash
cp api/series.py /path/to/your-project/app/api/series.py
```

### Step 2: Update Template
```bash
cp templates/series_detail.html /path/to/your-project/app/templates/series_detail.html
```

### Step 3: Update Main (if not done before)
```bash
# Make sure app/main.py includes:
from app.api import series
app.include_router(series.router, prefix="/api/series", tags=["series"])

# And has the frontend route:
@app.get("/series/{series_id}", response_class=HTMLResponse)
async def series_detail(request: Request, series_id: int):
    return templates.TemplateResponse("series_detail.html", {
        "request": request,
        "series_id": series_id
    })
```

### Step 4: Restart
```bash
python main.py
```

## Features Summary

### v4 Features (Filtering)
✅ Backend does all filtering using NON_PLAIN_FORMATS list  
✅ Frontend receives pre-categorized plain_issues, annuals, specials  
✅ Single source of truth for format categorization  
✅ Easy to add new formats (just update Python list)  

### v5 Features (Smart Tabs) NEW!
✅ Auto-detects standalone series (no plain issues)  
✅ Promotes all content to Issues tab for standalone series  
✅ Hides redundant Annuals/Specials tabs when not needed  
✅ Shows format badges even in Issues tab  
✅ Keeps Volumes tab for navigation  
✅ Backwards compatible with normal series  

## Format Handling

### NON_PLAIN_FORMATS List (in api/series.py)
```python
NON_PLAIN_FORMATS = [
    'annual',
    'giant-size',
    'graphic novel',
    'one shot',
    'one-shot',
    'hardcover',
    'limited series',
    'trade paperback',
    'tpb',
]
```

To add more formats, just update this list!

## Tab Logic

### Normal Series (has plain issues)
```
[Volumes] [Issues] [Annuals*] [Specials*] [Related] [Details]
          ↑ Plain   ↑ If exist ↑ If exist
```

### Standalone Series (no plain issues)
```
[Volumes] [Issues] [Related] [Details]
          ↑ Shows everything with badges
          (Annuals/Specials tabs hidden)
```

## Testing Scenarios

### Test 1: Standalone Graphic Novel
```
Series: Batman: The Killing Joke
- 1 volume, 1 issue (format="Graphic Novel")

Expected:
✓ Issues tab shows graphic novel with purple badge
✓ No Annuals tab
✓ No Specials tab
✓ Volumes tab present
```

### Test 2: Standalone One-Shots
```
Series: Superman: Red Son
- 1 volume, 3 issues (format="One-Shot")

Expected:
✓ Issues tab shows 3 one-shots with purple badges
✓ No Annuals tab
✓ No Specials tab
```

### Test 3: Normal Series
```
Series: Batman
- 5 volumes, 120 plain issues, 15 annuals, 8 specials

Expected:
✓ Issues tab shows 120 plain issues
✓ Annuals tab shows 15 annuals
✓ Specials tab shows 8 specials
✓ All tabs visible
```

### Test 4: Series with Annuals Only
```
Series: Amazing Spider-Man Annuals
- 1 volume, 5 annuals, no plain issues

Expected:
✓ Issues tab shows 5 annuals with yellow badges
✓ No Annuals tab (redundant)
✓ No Specials tab
```

## Visual Indicators

### In Issues Tab (Normal Series)
```
┌──────┐ ┌──────┐ ┌──────┐
│Cover │ │Cover │ │Cover │
│      │ │      │ │      │
└──────┘ └──────┘ └──────┘
Vol 1#1  Vol 1#2  Vol 1#3
(no badge - plain issues)
```

### In Issues Tab (Standalone Series)
```
┌──────────┐ ┌──────────┐
│  Cover   │ │  Cover   │
│[Graphic  │ │[One-Shot]│ ← Format badges
│ Novel]   │ │          │
└──────────┘ └──────────┘
The Killing  Red Son #1
Joke
```

## File Structure

```
series_v5_package/
├── api/
│   └── series.py              # Backend with filtering logic
├── templates/
│   └── series_detail.html     # Frontend with smart tab display
├── app_main.py                # Reference main.py with routes
├── README.md                  # This file
└── FILTERING_GUIDE.md         # Detailed v4 filtering explanation
```

## Common Issues

### Issue: Annuals/Specials tabs still showing for standalone series
**Cause:** Old template cached  
**Fix:** Hard refresh browser (Ctrl+Shift+R) or clear cache

### Issue: "Limited Series" still in Issues tab for normal series
**Cause:** Old API (v3 or earlier)  
**Fix:** Make sure using api/series.py from this package (v4+)

### Issue: Format badges not showing
**Cause:** CSS not loading  
**Fix:** Check Tailwind CSS is included in base.html

## Documentation

- **README.md** - This installation guide
- **FILTERING_GUIDE.md** - v4 filtering system (backend)
- Read both for complete understanding!

## Version History

- **v1-v3:** Initial implementation, JavaScript filtering (had bugs)
- **v4:** Backend filtering with NON_PLAIN_FORMATS list (fixed filtering)
- **v5:** Smart tab display for standalone series (fixed UX)

## Support

If you encounter issues:
1. Check browser console for JavaScript errors
2. Check server logs for API errors
3. Verify NON_PLAIN_FORMATS list matches your comics
4. Test with both normal and standalone series

## Next Steps

After installing:
1. Test with standalone graphic novel
2. Test with normal series
3. Add more formats to NON_PLAIN_FORMATS if needed
4. Build volume detail page (volumes currently link to /volumes/{id})

---

**Ready to deploy!** 🚀
