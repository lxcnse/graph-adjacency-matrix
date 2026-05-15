# MacierzGrafu

Implementacja **skierowanego grafu prostego** w Pythonie z wykorzystaniem zintegrowanej macierzy sąsiedztwa. Struktura danych łączy w jednej macierzy listy następników, nie-następników i poprzedników każdego wierzchołka.

---

## Opis struktury danych

Klasa `MacierzGrafu` przechowuje graf w macierzy `(V+2) × (V+2)`, gdzie `V` to liczba wierzchołków. Indeksy `0` i `V+1` pełnią role pomocnicze.

### Kodowanie w macierzy `M`

| Komórka | Znaczenie |
|---|---|
| `M[i][V+1]` | Głowa listy następników lub nie-następników wierzchołka `i` |
| `M[i][j] > 0` | `j` jest następnikiem `i`; wartość wskazuje na kolejny element listy |
| `M[i][j] < 0` | `j` jest nie-następnikiem `i`; wartość (zanegowana) wskazuje na kolejny element |
| `M[i][j] = 0` | Koniec listy |
| `M[j][0]` | Głowa listy poprzedników wierzchołka `j` |
| `M[0][j]` | Ostatni poprzednik wierzchołka `j` |

Poprzednicy przechowywani są w osobnej macierzy pomocniczej `_prev`, gdzie `_prev[i][j]` wskazuje na następny element listy poprzedników `j` po elemencie `i`.

---

## Wymagania

- Python 3.8+
- Brak zewnętrznych zależności

---

## Instalacja

```bash
git clone <url-repozytorium>
cd macierz-grafu
```

Żadna instalacja nie jest wymagana — wystarczy zaimportować klasę bezpośrednio.

---

## Szybki start

```python
from macierz_grafu import MacierzGrafu

g = MacierzGrafu(5)

g.dodaj_krawedz(1, 2)
g.dodaj_krawedz(1, 3)
g.dodaj_krawedz(2, 4)
g.dodaj_krawedz(3, 4)
g.dodaj_krawedz(4, 5)

print(g.nastepnicy(1))       # [2, 3]
print(g.poprzednicy(4))      # [2, 3]
print(g.nie_nastepnicy(1))   # [4, 5]
print(g.czy_krawedz(1, 2))   # True
print(g.czy_krawedz(1, 5))   # False

g.usun_krawedz(1, 3)
print(g.nastepnicy(1))       # [2]

print(g.krawedzie())
# [(1, 2), (2, 4), (3, 4), (4, 5)]

print(g)   # wyświetla macierz wewnętrzną
```

---

## API

### Konstruktor

```python
MacierzGrafu(v: int)
```

Tworzy pusty graf o `v` wierzchołkach (numerowanych `1..v`). Rzuca `ValueError` gdy `v < 1`.

---

### Zarządzanie krawędziami

```python
dodaj_krawedz(i: int, j: int) -> None
```
Dodaje krawędź skierowaną `i → j`. Rzuca `ValueError` gdy wierzchołki są poza zakresem, gdy `i == j` lub gdy krawędź już istnieje.

```python
usun_krawedz(i: int, j: int) -> None
```
Usuwa krawędź `i → j`. Rzuca `ValueError` gdy krawędź nie istnieje.

```python
czy_krawedz(i: int, j: int) -> bool
```
Zwraca `True` jeśli krawędź `i → j` istnieje.

---

### Zapytania o wierzchołki

```python
nastepnicy(i: int) -> List[int]
```
Posortowana lista wierzchołków `j` takich, że istnieje krawędź `i → j`.

```python
poprzednicy(j: int) -> List[int]
```
Posortowana lista wierzchołków `i` takich, że istnieje krawędź `i → j`.

```python
nie_nastepnicy(i: int) -> List[int]
```
Posortowana lista wierzchołków, do których z `i` nie prowadzi krawędź (z wyłączeniem samego `i`).

```python
stopien_wychodzacy(i: int) -> int
```
Liczba krawędzi wychodzących z `i`.

```python
stopien_wchodzacy(j: int) -> int
```
Liczba krawędzi wchodzących do `j`.

---

### Pozostałe

```python
krawedzie() -> List[Tuple[int, int]]
```
Posortowana lista wszystkich krawędzi w postaci par `(i, j)`.

```python
__str__() -> str
```
Reprezentacja tekstowa wewnętrznej macierzy — przydatna przy debugowaniu.

---

## Złożoność

| Operacja | Złożoność |
|---|---|
| `dodaj_krawedz` | O(V) |
| `usun_krawedz` | O(V) |
| `czy_krawedz` | O(deg⁺(i)) |
| `nastepnicy` | O(deg⁺(i) · log deg⁺(i)) |
| `poprzednicy` | O(deg⁻(j) · log deg⁻(j)) |
| `nie_nastepnicy` | O(V · log V) |
| `krawedzie` | O(E · log E) |
| Pamięć | O(V²) |

gdzie `deg⁺(i)` to stopień wychodzący, `deg⁻(j)` to stopień wchodzący, a `E` to liczba krawędzi.

---

## Ograniczenia

- Graf jest **skierowany** i **prosty** — nie obsługuje pętli własnych ani krawędzi wielokrotnych.
- Wierzchołki są numerowane od `1` do `V`; indeks `0` i `V+1` są zarezerwowane wewnętrznie.
- Rozmiar grafu jest ustalany przy tworzeniu i nie może być dynamicznie zmieniany.
