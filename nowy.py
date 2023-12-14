import numpy as np
import pandas as pd
from generator_a import generate_matrices
import sys
class GameTheory:
    def __init__(
        self,
        K,
        M,
        lista_podzadań,
        lista_kosztów_p,
        macierz_czasu_t_ij_podstawowa_z_daszkiem,
        T_0_deadline,
        M_0_deadline,
        w_m,
        w_t,
        q,
    ) -> None:
        self.K = K
        self.M = M
        self.lista_podzadań = lista_podzadań
        self.lista_kosztów_p = lista_kosztów_p
        self.macierz_czasu_t_ij_podstawowa_z_daszkiem = (
            macierz_czasu_t_ij_podstawowa_z_daszkiem
        )
        self.T_0_deadline = T_0_deadline
        self.M_0_deadline = M_0_deadline
        self.w_m = w_m
        self.w_t = w_t
        self.q = q

        self.macierz_czasu_t_policzona = None
        self.B = None

    def Funkcja_celu_Z(self,B) -> float:
        self.B = B
        pieniadz = self.koszty()
        koszt_czasu = self.T_turnaround()
        if not self.sprawdzenie_t_0:
            return (0,self.B,False)
        if not self.sprawdzenie_M_0:
            return (0,self.B,False)
            
        return (self.w_m * pieniadz + self.w_t * koszt_czasu, self.B, True)

    def sprawdzenie_t_0(self, turnaround):
        if turnaround > self.T_0_deadline:
            return False
        return True

    def sprawdzenie_M_0(self, pieniadz):
        if pieniadz > self.M_0_deadline:
            return False
        return True

    def koszty(self) -> float:
        suma = 0
        for i in range(self.K):
            for j in range(self.M):
                suma += (
                    self.lista_kosztów_p[j]
                    * self.macierz_czasu_t_ij_podstawowa_z_daszkiem[i][j]
                    * self.B[i][j]
                )
        return suma

    def wyznacz_t(self):
        jednoczesne_uzycia = [0] * self.M
        for i in self.B:
            for j in range(self.M):
                jednoczesne_uzycia[j] += i[j]
        macierz_czasu_t_policzona = [
            [row[i] * jednoczesne_uzycia[i] for i in range(len(jednoczesne_uzycia))]
            for row in self.macierz_czasu_t_ij_podstawowa_z_daszkiem
        ]
        for i in range(self.K):
            for j in range(self.M):
                macierz_czasu_t_policzona[i][j] = (
                    self.B[i][j] * macierz_czasu_t_policzona[i][j]
                )
        # print("macierz czasu t", pd.DataFrame(macierz_czasu_t_policzona))
        # print(
        #     "macierz czasu t^",
        #     pd.DataFrame(self.macierz_czasu_t_ij_podstawowa_z_daszkiem),
        # )
        return macierz_czasu_t_policzona

    def wyznacz_1_czesc(self):
        temp_b = np.array(self.B)
        temp_t_hat = np.array(self.macierz_czasu_t_ij_podstawowa_z_daszkiem)
        result = np.max(temp_b * temp_t_hat)
        # print(result)
        return result

    def wyznacz_2_czesc(self):
        result = 0
        # print(result)
        for l in range(1, self.q + 1):
            max_val = float("-inf")
            for i in range(self.K):
                for j in range(self.M):
                    term = self.B[i][j] * self.macierz_czasu_t_policzona[i][j] ** l
                    max_val = max(max_val, term)
            result += max_val
        return result

    # 4.3 12

    def T_turnaround(self):
        self.macierz_czasu_t_policzona = self.wyznacz_t()

        part1 = self.wyznacz_1_czesc()

        part2 = self.wyznacz_2_czesc()

        return part1 + part2




