"""
火星发展模拟器 — Mars Colony Simulator
=========================================
从第一批殖民者着陆到自给自足的火星文明

祝融号着陆点：乌托邦平原 (Utopia Planitia)
坐标：25.1N, 109.9E

"我们选择去火星，不是因为它容易，而是因为它难。"
                                    — JFK
"""

import time
import random
from dataclasses import dataclass, field
from typing import List

MARS_GRAVITY = 0.376
MARS_TEMP_AVG = -63
SOL_DURATION = 24.62

class Phase:
    LANDING  = "着陆期"
    SURVIVAL = "生存期"
    GROWTH   = "发展期"
    THRIVING = "繁荣期"

@dataclass
class MarsColony:
    name: str = "祝融基地"
    day: int = 0
    population: int = 12
    habitats: int = 3
    oxygen_plants: int = 2
    water_recyclers: int = 1
    greenhouses: int = 1
    solar_panels: int = 20
    food_reserve: float = 365.0
    water_reserve: float = 500.0
    oxygen_reserve: float = 200.0
    energy_output: float = 50.0
    morale: float = 80.0
    events: List[str] = field(default_factory=list)

    @property
    def phase(self) -> str:
        if self.day < 30:   return Phase.LANDING
        elif self.day < 90: return Phase.SURVIVAL
        elif self.day < 365: return Phase.GROWTH
        return Phase.THRIVING

    def daily_update(self):
        self.day += 1
        self.food_reserve -= self.population * 2.0 / 365
        self.water_reserve -= self.population * 0.02 * 0.1
        self.oxygen_reserve -= self.population * 0.84 / 1000

        dust = random.uniform(0.6, 1.0)
        self.energy_output = self.solar_panels * 2.5 * dust
        self.oxygen_reserve += self.oxygen_plants * 0.5
        self.food_reserve += self.greenhouses * 0.15
        self.water_reserve += self.water_recyclers * 0.08

        if self.food_reserve < 60:
            self.morale -= random.uniform(0.5, 2.0)
        if self.energy_output < 30:
            self.morale -= random.uniform(0.3, 1.5)
        if random.random() < 0.05:
            self.morale += random.uniform(1, 5)
        self.morale = max(0, min(100, self.morale))

        self._auto_build()
        if self.day % 30 == 0 or self.day == 1:
            self.events.append(f"Day{self.day}: {self.population}人 | 食物{self.food_reserve:.0f}d | 士气{self.morale:.0f}% | {self.phase}")
        self._check_milestones()

    def _auto_build(self):
        if self.phase == Phase.LANDING:
            if self.day == 5:
                self.greenhouses += 1
                self.events.append(f"Day{self.day}: 首个温室建成，种下第一批土豆")
            if self.day == 15:
                self.habitats += 1; self.solar_panels += 10
                self.events.append(f"Day{self.day}: 第二居住舱部署完成")
        elif self.phase == Phase.SURVIVAL:
            if self.day == 45 and self.solar_panels < 40:
                self.solar_panels += 15
                self.events.append(f"Day{self.day}: 太阳能阵列扩建 +15块")
            if self.day == 60 and self.water_recyclers < 3:
                self.water_recyclers += 1; self.oxygen_plants += 1
                self.events.append(f"Day{self.day}: 水循环/制氧系统升级")
        elif self.phase == Phase.GROWTH:
            if self.day == 100:
                self.population += 8; self.habitats += 2; self.greenhouses += 2
                self.events.append(f"Day{self.day}: 第二批殖民者抵达! +8人")
            if self.day == 180 and self.solar_panels < 80:
                self.solar_panels += 30
                self.events.append(f"Day{self.day}: 大型太阳能农场投运")
            if self.day == 250:
                self.population += 12; self.habitats += 3
                self.events.append(f"Day{self.day}: 第三批移民，殖民地破32人")
        elif self.phase == Phase.THRIVING:
            if self.day == 400:
                self.population += 20; self.habitats += 5; self.greenhouses += 5
                self.events.append(f"Day{self.day}: 火星首座穹顶城 '新长安' 封顶!")

    def _check_milestones(self):
        ms = {
            1: "祝融号着陆乌托邦平原",
            7: "完成首周生存实验",
            30: "通过第一个月极限考验",
            50: "首次火星土壤培育地球作物成功",
            100: "殖民地安全度过100火星日",
            200: "建成首个3D打印居住区",
            365: "火星一周年! 从生存迈向繁荣",
            500: "穹顶城正式命名: 新长安",
            687: "第一个火星年 — 殖民者超100人",
        }
        if self.day in ms:
            self.events.append(f"  [里程碑] Day{self.day}: {ms[self.day]}")

    def report(self):
        bar = int(self.morale // 5)
        print(f"\n  Mars Day {self.day} | {self.phase} | 人口{self.population}")
        print(f"  设施: {self.habitats}舱 {self.greenhouses}温室 {self.solar_panels}板 {self.energy_output:.0f}kW")
        print(f"  储备: 食物{self.food_reserve:.0f}d 水{self.water_reserve:.0f}t 氧{self.oxygen_reserve:.0f}t")
        print(f"  士气: {'|'*bar}{'.'*(20-bar)} {self.morale:.0f}%")

    def summary(self):
        print("\n  —— 殖民地编年史 ——\n")
        for e in self.events: print(f"    {e}")


def main():
    print(r"""
             .    '                   .    "
     .       .        *      .    '        .
  *       '      火星殖民模拟器 v1.0
     '      *   MARS COLONY SIMULATOR
        *    '
          """)
    colony = MarsColony()
    print(f"  初始: {colony.population}人着陆乌托邦平原\n")

    for _ in range(500):
        colony.daily_update()
        if colony.day % 10 == 0 or colony.day <= 5:
            colony.report()
        if colony.food_reserve <= 0:
            print("  [FAIL] 食物耗尽"); break
        if colony.morale <= 5:
            print("  [FAIL] 士气崩溃"); break
        time.sleep(0.01)

    ok = colony.phase == Phase.THRIVING and colony.population >= 30 and colony.morale >= 60
    print(f"\n  {'SUCCESS!' if ok else 'CONTINUE...'}")
    colony.summary()

if __name__ == "__main__":
    main()
