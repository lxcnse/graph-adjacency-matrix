import unittest
from macierz_grafu import MacierzGrafu


class TestInicjalizacja(unittest.TestCase):
    """Testy inicjalizacji struktury."""

    def test_tworzenie_jednego_wierzcholka(self):
        g = MacierzGrafu(1)
        self.assertEqual(g.V, 1)

    def test_tworzenie_wielu_wierzcholkow(self):
        g = MacierzGrafu(5)
        self.assertEqual(g.V, 5)

    def test_nieprawidlowa_liczba_wierzcholkow(self):
        with self.assertRaises(ValueError):
            MacierzGrafu(0)
        with self.assertRaises(ValueError):
            MacierzGrafu(-3)

    def test_poczatkowo_brak_krawedzi(self):
        g = MacierzGrafu(4)
        for i in range(1, 5):
            for j in range(1, 5):
                if i != j:
                    self.assertFalse(g.czy_krawedz(i, j),
                                     f"Oczekiwano braku krawędzi {i}→{j}")

    def test_macierz_ma_wymiar_v_plus_2(self):
        g = MacierzGrafu(3)
        self.assertEqual(len(g._m), 5)        # 3+2 wierszy
        self.assertEqual(len(g._m[0]), 5)     # 3+2 kolumn


class TestDodawanieKrawedzi(unittest.TestCase):
    """Testy dodawania krawędzi."""

    def setUp(self):
        self.g = MacierzGrafu(5)

    def test_dodaj_jedna_krawedz(self):
        self.g.dodaj_krawedz(1, 2)
        self.assertTrue(self.g.czy_krawedz(1, 2))

    def test_dodaj_wiele_krawedzi(self):
        krawedzie = [(1, 2), (1, 3), (2, 4), (3, 5), (4, 5)]
        for i, j in krawedzie:
            self.g.dodaj_krawedz(i, j)
        for i, j in krawedzie:
            self.assertTrue(self.g.czy_krawedz(i, j),
                            f"Brak krawędzi {i}→{j}")

    def test_dodaj_krawedz_nie_tworzy_odwrotnej(self):
        self.g.dodaj_krawedz(1, 2)
        self.assertFalse(self.g.czy_krawedz(2, 1))

    def test_dodaj_duplikat_rzuca_wyjatek(self):
        self.g.dodaj_krawedz(1, 2)
        with self.assertRaises(ValueError):
            self.g.dodaj_krawedz(1, 2)

    def test_petla_rzuca_wyjatek(self):
        with self.assertRaises(ValueError):
            self.g.dodaj_krawedz(3, 3)

    def test_poza_zakresem_rzuca_wyjatek(self):
        with self.assertRaises(ValueError):
            self.g.dodaj_krawedz(0, 1)
        with self.assertRaises(ValueError):
            self.g.dodaj_krawedz(1, 6)

    def test_dodaj_wszystkie_krawedzie_grafu_pelnego(self):
        g = MacierzGrafu(4)
        for i in range(1, 5):
            for j in range(1, 5):
                if i != j:
                    g.dodaj_krawedz(i, j)
        for i in range(1, 5):
            for j in range(1, 5):
                if i != j:
                    self.assertTrue(g.czy_krawedz(i, j))


class TestUsowanieKrawedzi(unittest.TestCase):
    """Testy usuwania krawędzi."""

    def setUp(self):
        self.g = MacierzGrafu(5)
        for i, j in [(1, 2), (1, 3), (2, 4), (3, 5), (4, 5)]:
            self.g.dodaj_krawedz(i, j)

    def test_usun_istniejaca_krawedz(self):
        self.g.usun_krawedz(1, 2)
        self.assertFalse(self.g.czy_krawedz(1, 2))

    def test_usun_nieistniejaca_rzuca_wyjatek(self):
        with self.assertRaises(ValueError):
            self.g.usun_krawedz(2, 1)

    def test_usun_i_dodaj_ponownie(self):
        self.g.usun_krawedz(1, 2)
        self.assertFalse(self.g.czy_krawedz(1, 2))
        self.g.dodaj_krawedz(1, 2)
        self.assertTrue(self.g.czy_krawedz(1, 2))

    def test_usun_wszystkie_krawedzie(self):
        krawedzie = [(1, 2), (1, 3), (2, 4), (3, 5), (4, 5)]
        for i, j in krawedzie:
            self.g.usun_krawedz(i, j)
        for i in range(1, 6):
            for j in range(1, 6):
                if i != j:
                    self.assertFalse(self.g.czy_krawedz(i, j))

    def test_usun_nie_narusza_innych_krawedzi(self):
        self.g.usun_krawedz(1, 2)
        self.assertTrue(self.g.czy_krawedz(1, 3))
        self.assertTrue(self.g.czy_krawedz(2, 4))
        self.assertTrue(self.g.czy_krawedz(3, 5))
        self.assertTrue(self.g.czy_krawedz(4, 5))


class TestNastepnicy(unittest.TestCase):
    """Testy pobierania listy następników."""

    def setUp(self):
        # Graf: 1→2, 1→3, 1→5, 2→3, 2→4, 3→4, 4→2, 4→3, 5→4
        self.g = MacierzGrafu(5)
        for i, j in [(1, 2), (1, 3), (1, 5), (2, 3), (2, 4), (3, 4), (4, 2), (4, 3), (5, 4)]:
            self.g.dodaj_krawedz(i, j)

    def test_nastepnicy_wierzcholka_z_wieloma_krawedziami(self):
        nastep = set(self.g.nastepnicy(1))
        self.assertEqual(nastep, {2, 3, 5})

    def test_nastepnicy_wierzcholka_bez_krawedzi_wychodzacych(self):
        g = MacierzGrafu(3)
        g.dodaj_krawedz(1, 2)
        nastep = self.g.nastepnicy(3)  # 3 nie ma następników wychodzących z 3
        # W setUp: 3→4, więc 3 ma następnika
        self.assertIn(4, set(self.g.nastepnicy(3)))

    def test_nastepnicy_izolowanego_wierzcholka(self):
        g = MacierzGrafu(4)
        g.dodaj_krawedz(1, 2)
        self.assertEqual(g.nastepnicy(3), [])
        self.assertEqual(g.nastepnicy(4), [])

    def test_nastepnicy_po_usunieciu_krawedzi(self):
        self.g.usun_krawedz(1, 3)
        nastep = set(self.g.nastepnicy(1))
        self.assertEqual(nastep, {2, 5})
        self.assertNotIn(3, nastep)

    def test_nastepnicy_pelny_graf(self):
        g = MacierzGrafu(4)
        for i in range(1, 5):
            for j in range(1, 5):
                if i != j:
                    g.dodaj_krawedz(i, j)
        for i in range(1, 5):
            expected = {j for j in range(1, 5) if j != i}
            self.assertEqual(set(g.nastepnicy(i)), expected)


class TestPoprzednicy(unittest.TestCase):
    """Testy pobierania listy poprzedników."""

    def setUp(self):
        # Graf skierowany z rys. 2 (wg algorytm.org): 1→2,1→3,2→4,3→2,3→4,4→5,5→1
        self.g = MacierzGrafu(5)
        for i, j in [(1, 2), (1, 3), (2, 4), (3, 2), (3, 4), (4, 5), (5, 1)]:
            self.g.dodaj_krawedz(i, j)

    def test_poprzednicy_wierzcholka_2(self):
        prev = set(self.g.poprzednicy(2))
        self.assertEqual(prev, {1, 3})

    def test_poprzednicy_wierzcholka_1(self):
        prev = set(self.g.poprzednicy(1))
        self.assertEqual(prev, {5})

    def test_poprzednicy_wierzcholka_bez_poprzednikow(self):
        # Wierzchołek 3 ma poprzednika: tylko 1
        prev = set(self.g.poprzednicy(3))
        self.assertEqual(prev, {1})

    def test_poprzednicy_po_dodaniu_krawedzi(self):
        self.g.dodaj_krawedz(2, 1)
        prev = set(self.g.poprzednicy(1))
        self.assertIn(2, prev)
        self.assertIn(5, prev)

    def test_poprzednicy_po_usunieciu_krawedzi(self):
        self.g.usun_krawedz(1, 2)
        prev = set(self.g.poprzednicy(2))
        self.assertNotIn(1, prev)
        self.assertIn(3, prev)


class TestStopnie(unittest.TestCase):
    """Testy obliczania stopni wierzchołków."""

    def setUp(self):
        self.g = MacierzGrafu(5)
        for i, j in [(1, 2), (1, 3), (1, 5), (2, 3), (2, 4), (3, 4), (4, 2), (4, 3), (5, 4)]:
            self.g.dodaj_krawedz(i, j)

    def test_stopien_wychodzacy(self):
        self.assertEqual(self.g.stopien_wychodzacy(1), 3)  # 1→2,3,5
        self.assertEqual(self.g.stopien_wychodzacy(2), 2)  # 2→3,4
        self.assertEqual(self.g.stopien_wychodzacy(3), 1)  # 3→4
        self.assertEqual(self.g.stopien_wychodzacy(4), 2)  # 4→2,3
        self.assertEqual(self.g.stopien_wychodzacy(5), 1)  # 5→4

    def test_stopien_wchodzacy(self):
        self.assertEqual(self.g.stopien_wchodzacy(2), 2)  # ←1, ←4
        self.assertEqual(self.g.stopien_wchodzacy(3), 3)  # ←1, ←2, ←4
        self.assertEqual(self.g.stopien_wchodzacy(4), 3)  # ←2, ←3, ←5
        self.assertEqual(self.g.stopien_wchodzacy(1), 0)  # brak poprzedników
        self.assertEqual(self.g.stopien_wchodzacy(5), 1)  # ←1

    def test_stopien_izolowanego_wierzcholka(self):
        g = MacierzGrafu(5)
        g.dodaj_krawedz(1, 2)
        self.assertEqual(g.stopien_wychodzacy(3), 0)
        self.assertEqual(g.stopien_wchodzacy(3), 0)

    def test_stopien_po_usunieciu_krawedzi(self):
        self.g.usun_krawedz(1, 2)
        self.assertEqual(self.g.stopien_wychodzacy(1), 2)
        self.assertEqual(self.g.stopien_wchodzacy(2), 1)  # tylko ←4


class TestKrawedzie(unittest.TestCase):
    """Testy listy wszystkich krawędzi."""

    def test_krawedzie_puste(self):
        g = MacierzGrafu(4)
        self.assertEqual(g.krawedzie(), [])

    def test_krawedzie_jedna(self):
        g = MacierzGrafu(3)
        g.dodaj_krawedz(2, 3)
        self.assertEqual(set(g.krawedzie()), {(2, 3)})

    def test_krawedzie_wiele(self):
        g = MacierzGrafu(4)
        oczekiwane = {(1, 2), (1, 3), (2, 4), (3, 4)}
        for i, j in oczekiwane:
            g.dodaj_krawedz(i, j)
        self.assertEqual(set(g.krawedzie()), oczekiwane)

    def test_krawedzie_po_usunach(self):
        g = MacierzGrafu(4)
        for i, j in [(1, 2), (1, 3), (2, 4)]:
            g.dodaj_krawedz(i, j)
        g.usun_krawedz(1, 3)
        self.assertEqual(set(g.krawedzie()), {(1, 2), (2, 4)})


class TestGrafyZPrzykladow(unittest.TestCase):

    def _zbuduj_graf_rys2(self) -> MacierzGrafu:
        """Graf skierowany: 1→2, 1→3, 2→4, 3→2, 3→4, 4→5, 5→1"""
        g = MacierzGrafu(5)
        for i, j in [(1, 2), (1, 3), (2, 4), (3, 2), (3, 4), (4, 5), (5, 1)]:
            g.dodaj_krawedz(i, j)
        return g

    def test_poprawnosc_grafu_rys2(self):
        g = self._zbuduj_graf_rys2()
        # Sprawdź istniejące krawędzie
        istniejace = [(1, 2), (1, 3), (2, 4), (3, 2), (3, 4), (4, 5), (5, 1)]
        for i, j in istniejace:
            self.assertTrue(g.czy_krawedz(i, j), f"Brak krawędzi {i}→{j}")
        # Sprawdź brak pozostałych
        wszystkie = [(i, j) for i in range(1, 6) for j in range(1, 6) if i != j]
        brakujace = set(wszystkie) - set(istniejace)
        for i, j in brakujace:
            self.assertFalse(g.czy_krawedz(i, j), f"Nieoczekiwana krawędź {i}→{j}")

    def test_nastepnicy_grafu_rys2(self):
        g = self._zbuduj_graf_rys2()
        self.assertEqual(set(g.nastepnicy(1)), {2, 3})
        self.assertEqual(set(g.nastepnicy(2)), {4})
        self.assertEqual(set(g.nastepnicy(3)), {2, 4})
        self.assertEqual(set(g.nastepnicy(4)), {5})
        self.assertEqual(set(g.nastepnicy(5)), {1})

    def test_poprzednicy_grafu_rys2(self):
        g = self._zbuduj_graf_rys2()
        self.assertEqual(set(g.poprzednicy(1)), {5})
        self.assertEqual(set(g.poprzednicy(2)), {1, 3})
        self.assertEqual(set(g.poprzednicy(3)), {1})
        self.assertEqual(set(g.poprzednicy(4)), {2, 3})
        self.assertEqual(set(g.poprzednicy(5)), {4})

    def test_stopnie_grafu_rys2(self):
        g = self._zbuduj_graf_rys2()
        # Stopnie wychodzące
        self.assertEqual(g.stopien_wychodzacy(1), 2)
        self.assertEqual(g.stopien_wychodzacy(2), 1)
        self.assertEqual(g.stopien_wychodzacy(3), 2)
        self.assertEqual(g.stopien_wychodzacy(4), 1)
        self.assertEqual(g.stopien_wychodzacy(5), 1)
        # Stopnie wchodzące
        self.assertEqual(g.stopien_wchodzacy(1), 1)
        self.assertEqual(g.stopien_wchodzacy(2), 2)
        self.assertEqual(g.stopien_wchodzacy(3), 1)
        self.assertEqual(g.stopien_wchodzacy(4), 2)
        self.assertEqual(g.stopien_wchodzacy(5), 1)

    def test_dynamiczne_modyfikacje(self):
        """Test serii dodań i usunięć krawędzi."""
        g = self._zbuduj_graf_rys2()
        # Dodaj krawędź 2→3
        g.dodaj_krawedz(2, 3)
        self.assertTrue(g.czy_krawedz(2, 3))
        self.assertIn(3, g.nastepnicy(2))
        self.assertIn(2, g.poprzednicy(3))
        # Usuń krawędź 1→2
        g.usun_krawedz(1, 2)
        self.assertFalse(g.czy_krawedz(1, 2))
        self.assertNotIn(2, g.nastepnicy(1))
        self.assertNotIn(1, g.poprzednicy(2))
        # Dodaj ponownie krawędź 1→2
        g.dodaj_krawedz(1, 2)
        self.assertTrue(g.czy_krawedz(1, 2))

    def test_walidacja_zakres(self):
        g = self._zbuduj_graf_rys2()
        with self.assertRaises(ValueError):
            g.czy_krawedz(0, 1)
        with self.assertRaises(ValueError):
            g.nastepnicy(6)
        with self.assertRaises(ValueError):
            g.poprzednicy(0)


class TestWielkiGraf(unittest.TestCase):
    """Test wydajnościowy na większym grafie."""

    def test_graf_10_wierzcholkow_pelny(self):
        n = 10
        g = MacierzGrafu(n)
        krawedzie = []
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if i != j:
                    g.dodaj_krawedz(i, j)
                    krawedzie.append((i, j))
        self.assertEqual(len(g.krawedzie()), n * (n - 1))
        for i in range(1, n + 1):
            self.assertEqual(g.stopien_wychodzacy(i), n - 1)
            self.assertEqual(g.stopien_wchodzacy(i), n - 1)

    def test_dodaj_usun_na_przemian(self):
        g = MacierzGrafu(6)
        for _ in range(3):
            g.dodaj_krawedz(1, 2)
            self.assertTrue(g.czy_krawedz(1, 2))
            g.usun_krawedz(1, 2)
            self.assertFalse(g.czy_krawedz(1, 2))


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in [
        TestInicjalizacja,
        TestDodawanieKrawedzi,
        TestUsowanieKrawedzi,
        TestNastepnicy,
        TestPoprzednicy,
        TestStopnie,
        TestKrawedzie,
        TestGrafyZPrzykladow,
        TestWielkiGraf,
    ]:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    import sys
    sys.exit(0 if result.wasSuccessful() else 1)