from functools import lru_cache
from typing import Sequence, Union

NumberList = Sequence[Union[int, float]]


class TrendAdjustedExponentialSmoothing:
    def __init__(
        self, values: NumberList, alpha: float, beta: float, log_outputs: bool = False
    ) -> None:
        self.values = values
        self.alpha = alpha
        self.beta = beta
        self.log_outputs = log_outputs

    def get_constants(self):
        return self.values, self.alpha, self.beta

    def log(self, text: str):
        if self.log_outputs:
            print(text)

    @lru_cache()
    def smooth(self, t: int) -> float:
        values, alpha, _ = self.get_constants()

        if t == 0:
            st = values[t]
            self.log(f"S{t + 1} = {st}\n")
            return st

        previous_st = self.smooth(t - 1)
        adjusted_trend = self.adjust_trend(t - 1)

        st = (alpha * values[t]) + ((1 - alpha) * (previous_st + adjusted_trend))

        self.log(f"S{t + 1} = (alpha * Y(t)) + ((1 - alpha) * (S({t}) + M({t})))")
        self.log(
            f"S{t + 1} = ({alpha} * {values[t]}) + ((1 - {alpha}) * ({previous_st} + {adjusted_trend})) = {st}\n"
        )

        return st

    @lru_cache()
    def adjust_trend(self, t: int) -> float:
        values, _, beta = self.get_constants()

        if t == 0:
            mt = values[t + 1] - values[t]
            self.log(f"M{t + 1} = {mt}\n")
            return mt

        st = self.smooth(t)
        previous_st = self.smooth(t - 1)
        adjusted_trend = self.adjust_trend(t - 1)

        mt = (beta * (st - previous_st)) + ((1 - beta) * adjusted_trend)

        self.log(f"M{t + 1} = (beta * (S({t + 1}) - S({t}))) + ((1 - beta) * M({t}))")
        self.log(
            f"M{t + 1} = ({beta} * ({st} - {previous_st})) + ((1 - {beta}) * {adjusted_trend}) = {mt}"
        )

        return mt

    def __call__(self, t: int) -> float:
        values, alpha, beta = self.get_constants()

        self.log(f"{values=}")
        self.log(f"{alpha=}")
        self.log(f"{beta=}")

        s = self.smooth(t - 1)
        m = self.adjust_trend(t - 1)

        self.log(f"F({t}) = S({t}) + M({t})")
        self.log(f"F({t}) = {s} + {m}")

        return s + m


def main():
    values = [5, 10, 15, 25, 20]
    alpha = 0.5
    beta = 0.5
    t = len(values) + 1

    algorithm = TrendAdjustedExponentialSmoothing(values, alpha, beta, True)
    print(algorithm(t))


if __name__ == "__main__":
    main()
