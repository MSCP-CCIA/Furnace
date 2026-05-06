from furnace import OptimizationStudy


def main() -> None:
    study = OptimizationStudy.from_config("configs/default.yaml")
    study.run()


if __name__ == "__main__":
    main()
