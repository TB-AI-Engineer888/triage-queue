from collections import deque
from datetime import datetime

LEVELS = (1, 2, 3)


class Patient:
    def __init__(self, name, triage_level, arrived_at):
        self.name = name
        self.triage_level = triage_level
        self.arrived_at = arrived_at

    def __str__(self):
        arrived = self.arrived_at.isoformat(sep=" ", timespec="seconds")
        return f"{self.name}  {self.triage_level}  {arrived}"


class TriageQueue:
    def __init__(self):
        self._queues = {level: deque() for level in LEVELS}

    def enqueue(self, patient):
        level = patient.triage_level
        if level not in self._queues:
            raise ValueError(
                f"Invalid triage level: {level}. Valid triage levels: 1, 2, 3."
            )
        self._queues[level].append(patient)
        return patient

    def dequeue(self):
        queue = self._next_queue()
        if queue is None:
            raise ValueError("No patient is waiting.")
        return queue.popleft()

    def peek(self):
        queue = self._next_queue()
        if queue is None:
            return None
        return queue[0]

    def list_queue(self):
        waiting = []
        for level in LEVELS:
            waiting.extend(self._queues[level])
        return waiting

    def stats(self):
        return {level: len(self._queues[level]) for level in LEVELS}

    def _next_queue(self):
        for level in LEVELS:
            if self._queues[level]:
                return self._queues[level]
        return None


def _prompt(text):
    try:
        return input(text).strip()
    except EOFError:
        print()
        return None


def _read_level():
    raw = _prompt("Triage level (1, 2, 3): ")
    if raw is None:
        return None
    try:
        level = int(raw)
    except ValueError:
        print(f"Invalid triage level: {raw}. Valid triage levels: 1, 2, 3.")
        return False
    if level not in LEVELS:
        print(f"Invalid triage level: {level}. Valid triage levels: 1, 2, 3.")
        return False
    return level


def _print_queue(waiting):
    if not waiting:
        print("No patient is waiting.")
        return
    for patient in waiting:
        print(patient)


def _print_stats(counts):
    for level in LEVELS:
        print(f"{level}: {counts[level]}")


def main():
    queue = TriageQueue()
    while True:
        print()
        print("1. Add a new patient")
        print("2. Call the next patient")
        print("3. View the current queue")
        print("4. See queue stats")
        print("0. Exit")
        choice = _prompt("Select: ")
        if choice is None or choice == "0":
            return
        if choice == "1":
            name = _prompt("Name: ")
            if name is None:
                return
            level = _read_level()
            if level is None:
                return
            if level is False:
                continue
            patient = queue.enqueue(Patient(name, level, datetime.now()))
            print(patient)
        elif choice == "2":
            try:
                patient = queue.dequeue()
            except ValueError as error:
                print(error)
                continue
            print(patient)
        elif choice == "3":
            _print_queue(queue.list_queue())
        elif choice == "4":
            _print_stats(queue.stats())
        else:
            print("Invalid option.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
