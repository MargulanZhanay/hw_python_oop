from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Informational message about the workout."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Base training class."""
    H_IN_MIN = 60  # Hours into minutes.
    M_IN_KM = 1000  # Meter to km.
    LEN_STEP = 0.65  # Length of the step in meters.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get the average movement speed."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get the number of calories burned."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Return an informational message about the completed workout."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Workout: running."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Get the number of calories burned from running."""
        duration_in_min: float = self.duration * self.H_IN_MIN  # Training
        # time in minutes.
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * duration_in_min)


class SportsWalking(Training):
    """Training: walking."""
    K_1 = 0.035  # Coefficient for counting calories.
    K_2 = 0.029  # Coefficient for counting calories.
    KMH_IN_MS = 0.278  # Km/h to m/sec.
    CM_IN_M = 100  # Centimetres to meters

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Get the number of calories burned from walking."""
        return ((self.K_1 * self.weight + ((self.get_mean_speed()
                * self.KMH_IN_MS)**2 / (self.height
                / self.CM_IN_M)) * self.K_2 * self.weight)
                * (self.duration * self.H_IN_MIN))


class Swimming(Training):
    """Training: swimming."""
    LEN_STEP = 1.38  # Length of the stroke in meters.
    AV_SPEED_VAL = 1.1
    SPEED_MULTIPLIER = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Get the average movement speed when swimming."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Get the number of calories burned from swimming."""
        return ((self.get_mean_speed() + self.AV_SPEED_VAL)
                * self.SPEED_MULTIPLIER * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Read the data received from the sensors."""
    commands = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return commands[workout_type](*data)


def main(training: Training) -> None:
    """Main function."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
