from typing import List, Optional, Set, Tuple


class MacierzGrafu:

    def __init__(self, v: int):
        """
        Tworzy pustą MacierzGrafu dla grafu o V wierzchołkach.

        :param v: liczba wierzchołków (≥ 1)
        """
        if v < 1:
            raise ValueError("Liczba wierzchołków musi być ≥ 1")
        self.V = v
        self._size = v + 2  # indeksy 0..V+1

        # Główna macierz (V+2)×(V+2)
        self._m: List[List[int]] = [[0] * self._size for _ in range(self._size)]

        # Pomocnicza macierz do przechowywania łańcucha poprzedników
        # _prev[i][j] = następny poprzednik j po i (lub 0 = koniec)
        # Głowa listy poprzedników j: _m[j][0]
        # Ostatni poprzednik j: _m[0][j]
        # Łańcuch: _m[j][0] → _prev[p1][j] → _prev[p2][j] → ... → 0
        self._prev: List[List[int]] = [[0] * self._size for _ in range(self._size)]

        # Inicjalizacja: dla każdego i, wszystkie j≠i są nie-następnikami
        self._inicjuj_listy_nie_nastepnikow()


    def _inicjuj_listy_nie_nastepnikow(self):
        """
        Buduje łańcuch nie-następników dla każdego wierzchołka i.

        Łańcuch: M[i][V+1] = -n1,  M[i][n1] = -n2,  ...,  M[i][nk] = 0
        gdzie n1, n2, ..., nk = {1..V} / {i}.
        """
        V = self.V
        for i in range(1, V + 1):
            nienas = [j for j in range(1, V + 1) if j != i]
            if not nienas:
                continue
            self._m[i][V + 1] = -nienas[0]
            for k in range(len(nienas) - 1):
                self._m[i][nienas[k]] = -nienas[k + 1]
            self._m[i][nienas[-1]] = 0  # koniec listy


    def dodaj_krawedz(self, i: int, j: int):
        """
        Dodaje krawędź skierowaną i → j.

        :raises ValueError: jeśli i lub j poza zakresem, i==j, lub krawędź istnieje
        """
        self._waliduj(i, j)
        if self.czy_krawedz(i, j):
            raise ValueError(f"Krawędź {i}→{j} już istnieje")

        self._usun_z_nie_nastepnikow(i, j)
        self._dol_do_nastepnikow(i, j)
        self._dol_do_poprzednikow(i, j)

    def usun_krawedz(self, i: int, j: int):
        """
        Usuwa krawędź skierowaną i → j.

        :raises ValueError: jeśli krawędź nie istnieje
        """
        self._waliduj(i, j)
        if not self.czy_krawedz(i, j):
            raise ValueError(f"Krawędź {i}→{j} nie istnieje")

        self._usun_z_nastepnikow(i, j)
        self._dol_do_nie_nastepnikow(i, j)
        self._usun_z_poprzednikow(i, j)

    def czy_krawedz(self, i: int, j: int) -> bool:
        """
        Sprawdza czy istnieje krawędź i → j.
        Korzysta z przejścia listy następników.
        """
        self._waliduj(i, j)
        return j in self._zbior_nastepnikow(i)


    def nastepnicy(self, i: int) -> List[int]:
        """Zwraca posortowaną listę następników wierzchołka i."""
        self._waliduj_jeden(i)
        return sorted(self._zbior_nastepnikow(i))

    def poprzednicy(self, j: int) -> List[int]:
        """Zwraca posortowaną listę poprzedników wierzchołka j."""
        self._waliduj_jeden(j)
        wynik = []
        current = self._m[j][0]
        visited = set()
        while current != 0 and current not in visited:
            wynik.append(current)
            visited.add(current)
            current = self._prev[current][j]
        return sorted(wynik)

    def nie_nastepnicy(self, i: int) -> List[int]:
        """Zwraca posortowaną listę nie-następników wierzchołka i (wierzchołki poza i)."""
        self._waliduj_jeden(i)
        nastep = self._zbior_nastepnikow(i)
        return sorted(j for j in range(1, self.V + 1) if j != i and j not in nastep)

    def stopien_wychodzacy(self, i: int) -> int:
        """Liczba krawędzi wychodzących z i."""
        self._waliduj_jeden(i)
        return len(self._zbior_nastepnikow(i))

    def stopien_wchodzacy(self, j: int) -> int:
        """Liczba krawędzi wchodzących do j."""
        return len(self.poprzednicy(j))

    def krawedzie(self) -> List[Tuple[int, int]]:
        """Zwraca posortowaną listę wszystkich krawędzi (i, j)."""
        result = []
        for i in range(1, self.V + 1):
            for j in sorted(self._zbior_nastepnikow(i)):
                result.append((i, j))
        return result


    def __str__(self) -> str:
        V = self.V
        s = self._size
        naglowek = "     " + "".join(f"{j:4d}" for j in range(s))
        sep = "     " + "─" * (4 * s)
        wiersze = [naglowek, sep]
        for i in range(s):
            vals = "".join(f"{self._m[i][j]:4d}" for j in range(s))
            wiersze.append(f"{i:3d} │ {vals}")
        return "\n".join(wiersze)



    def _waliduj(self, i: int, j: int):
        if not (1 <= i <= self.V):
            raise ValueError(f"Wierzchołek {i} poza zakresem [1, {self.V}]")
        if not (1 <= j <= self.V):
            raise ValueError(f"Wierzchołek {j} poza zakresem [1, {self.V}]")
        if i == j:
            raise ValueError("Pętle własne nie są obsługiwane")

    def _waliduj_jeden(self, i: int):
        if not (1 <= i <= self.V):
            raise ValueError(f"Wierzchołek {i} poza zakresem [1, {self.V}]")



    def _zbior_nastepnikow(self, i: int) -> Set[int]:
        """Przechodzi łańcuch następników wiersza i i zwraca zbiór."""
        V = self.V
        wynik: Set[int] = set()
        ptr = self._m[i][V + 1]
        if ptr <= 0:
            return wynik
        current = ptr
        seen = set()
        while current > 0 and current not in seen:
            wynik.add(current)
            seen.add(current)
            current = self._m[i][current]
        return wynik

    def _ostatni_nastepnik(self, i: int) -> Optional[int]:
        """Zwraca indeks ostatniego następnika i, lub None jeśli brak."""
        V = self.V
        ptr = self._m[i][V + 1]
        if ptr <= 0:
            return None
        current = ptr
        seen = set()
        while self._m[i][current] > 0 and self._m[i][current] not in seen:
            seen.add(current)
            current = self._m[i][current]
        return current


    def _dol_do_nastepnikow(self, i: int, j: int):
        """
        Dołącza j na koniec listy następników i.
        Wartość M[i][j] staje się wartością M[i][ostatni_nast]
        (zachowanie wskaźnika do listy nie-następników lub 0).
        """
        V = self.V
        ostatni = self._ostatni_nastepnik(i)
        if ostatni is None:
            # Brak poprzednich następników: j staje się pierwszym
            stary_ptr = self._m[i][V + 1]   # ≤ 0 (głowa nie-następników lub 0)
            self._m[i][V + 1] = j
            self._m[i][j] = stary_ptr        # j dziedziczy wskaźnik do nie-następników
        else:
            stary_ptr = self._m[i][ostatni]  # ≤ 0
            self._m[i][ostatni] = j
            self._m[i][j] = stary_ptr

    def _usun_z_nastepnikow(self, i: int, j: int):
        """Usuwa j z łańcucha następników i."""
        V = self.V
        ptr = self._m[i][V + 1]
        if ptr <= 0:
            return

        if ptr == j:
            nxt = self._m[i][j]
            self._m[i][V + 1] = nxt   # może być > 0 (kolejny nast.) lub ≤ 0
            self._m[i][j] = 0
            return

        prev = ptr
        current = self._m[i][prev]
        seen = {prev}
        while current > 0 and current != j and current not in seen:
            seen.add(current)
            prev = current
            current = self._m[i][current]

        if current == j:
            nxt = self._m[i][j]
            self._m[i][prev] = nxt
            self._m[i][j] = 0


    def _glowa_nie_nastepnikow(self, i: int) -> int:
        """Zwraca indeks pierwszego nie-następnika i (lub 0 jeśli brak)."""
        V = self.V
        ostatni = self._ostatni_nastepnik(i)
        if ostatni is None:
            ptr = self._m[i][V + 1]
        else:
            ptr = self._m[i][ostatni]
        return -ptr if ptr < 0 else 0

    def _wskaznik_na_glowe_nie_nastepnikow(self, i: int) -> Tuple[Optional[int], str]:
        """
        Zwraca (węzeł_wskazujący_na_głowę, typ).
        typ = 'glowna' jeśli wskaźnik jest w M[i][V+1],
              'nastepnik' jeśli wskaźnik jest w M[i][ostatni_nastepnik].
        """
        V = self.V
        ostatni = self._ostatni_nastepnik(i)
        if ostatni is None:
            return None, 'glowna'  # wskaźnik jest w M[i][V+1]
        else:
            return ostatni, 'nastepnik'

    def _ustaw_glowe_nie_nastepnikow(self, i: int, val: int):
        """Ustawia wskaźnik głowy listy nie-następników i na val (≤ 0)."""
        V = self.V
        ostatni = self._ostatni_nastepnik(i)
        if ostatni is None:
            self._m[i][V + 1] = val
        else:
            self._m[i][ostatni] = val

    def _usun_z_nie_nastepnikow(self, i: int, j: int):
        """
        Usuwa j z łańcucha nie-następników i.
        j musi być w liście (M[i][j] ≤ 0).
        """
        glowa = self._glowa_nie_nastepnikow(i)
        if glowa == 0:
            return

        if glowa == j:
            nxt = self._m[i][j]   # ≤ 0 (następny nie-nastep.) lub 0
            self._ustaw_glowe_nie_nastepnikow(i, nxt)
            self._m[i][j] = 0
            return

        prev = glowa
        current_raw = self._m[i][glowa]
        current = -current_raw if current_raw < 0 else 0
        seen = {glowa}

        while current != 0 and current != j and current not in seen:
            seen.add(current)
            prev = current
            current_raw = self._m[i][current]
            current = -current_raw if current_raw < 0 else 0

        if current == j:
            nxt = self._m[i][j]      # ≤ 0
            self._m[i][prev] = nxt   # prev wskazuje teraz na następnika j
            self._m[i][j] = 0

    def _dol_do_nie_nastepnikow(self, i: int, j: int):
        """Dołącza j na koniec listy nie-następników i."""
        glowa = self._glowa_nie_nastepnikow(i)

        if glowa == 0:
            self._ustaw_glowe_nie_nastepnikow(i, -j)
            self._m[i][j] = 0
            return

        # Znajdź ostatni nie-następnik
        current = glowa
        seen = set()
        while True:
            seen.add(current)
            nxt_raw = self._m[i][current]
            if nxt_raw >= 0:   # 0 = koniec, > 0 nie powinno wystąpić tu
                break
            nxt = -nxt_raw
            if nxt in seen:
                break
            current = nxt

        self._m[i][current] = -j
        self._m[i][j] = 0


    def _dol_do_poprzednikow(self, i: int, j: int):
        """
        Dodaje i na początku listy poprzedników j.
        Łańcuch w _prev: _prev[i][j] = stara głowa.
        """
        stara_glowa = self._m[j][0]
        self._m[j][0] = i
        self._prev[i][j] = stara_glowa
        if stara_glowa == 0:
            self._m[0][j] = i

    def _usun_z_poprzednikow(self, i: int, j: int):
        """Usuwa i z listy poprzedników j."""
        glowa = self._m[j][0]
        if glowa == 0:
            return

        if glowa == i:
            nxt = self._prev[i][j]
            self._m[j][0] = nxt
            if nxt == 0:
                self._m[0][j] = 0
            self._prev[i][j] = 0
            return

        prev = glowa
        current = self._prev[glowa][j]
        seen = {glowa}

        while current != 0 and current != i and current not in seen:
            seen.add(current)
            prev = current
            current = self._prev[current][j]

        if current == i:
            nxt = self._prev[i][j]
            self._prev[prev][j] = nxt
            if nxt == 0:
                self._m[0][j] = prev
            self._prev[i][j] = 0