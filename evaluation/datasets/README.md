# Evaluation datasets

One CSV per language (`en.csv`, `pt.csv`, `es.csv`), 50 rows each: 25 `sale` and 25 `rent`.
The last rows of each shuffle include edge cases with missing optional fields
(no neighborhood, no price, no floor/year, no bedrooms/bathrooms, no area/amenities).
The data is synthetic.

## Columns

Input columns map 1:1 to `PropertyData` in `app/models.py`. An empty cell means `null`.

| Column | Type | Maps to |
|---|---|---|
| `title` | text | `title` |
| `city` | text | `location.city` |
| `neighborhood` | text, optional | `location.neighborhood` |
| `bedrooms`, `bathrooms`, `floor`, `year_built` | integer, optional | `features.*` |
| `area_sqm` | number, optional | `features.area_sqm` |
| `balcony`, `parking`, `elevator` | `True`/`False`, optional | `features.*` |
| `price` | number, optional | `price` |
| `listing_type` | `sale` or `rent` | `listing_type` |
| `language` | `en`, `pt` or `es` | `language` |

Expected column:

| Column | Meaning |
|---|---|
| `expected_facts` | Numbers from the input that the listing should mention (bedrooms, bathrooms, area, floor, year, price), separated by `\|`. Missing fields are left out. |

Load them with `evaluation.dataset.load_rows("en")`.
