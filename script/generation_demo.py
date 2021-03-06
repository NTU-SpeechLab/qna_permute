import os

from qgen.encoder.universal_sentence_encoder import USEEncoder
from qgen.generator import FPMGenerator, SymSubGenerator, IMTGenerator, ZeroShotGenerator, EDAGenerator

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

AQA_PATH = os.path.join(ROOT_PATH, 'active-qa')
AQA_CONFIG_PATH = os.path.join(ROOT_PATH, 'config/aqa.json')
AQA_MODEL_PATH = os.path.join(ROOT_PATH, 'model/pretrained/active-qa/translate.ckpt-1460356')
AQA_RL_MODEL_PATH = os.path.join(ROOT_PATH, 'model/pretrained/active-qa/translate.ckpt-6156696')
# IMT_PATH = os.path.join(ROOT_PATH, 'model/onmt_model_step_15000.pt')
ONMT_PATH = os.path.join(ROOT_PATH, 'OpenNMT-py')
USE_PATH = os.path.join(ROOT_PATH, 'model/pretrained/universal_sentence_encoder')


def main():
    print("Initializing...")
    fpm = FPMGenerator()
    symsub = SymSubGenerator(USEEncoder(USE_PATH))
    # imt = IMTGenerator(ONMT_PATH, IMT_PATH, n_best=5)
    zeroshot = ZeroShotGenerator(AQA_PATH, AQA_CONFIG_PATH, AQA_MODEL_PATH)
    zeroshot_rl = ZeroShotGenerator(AQA_PATH, AQA_CONFIG_PATH, AQA_RL_MODEL_PATH)
    eda = EDAGenerator()

    generator = None
    while True:
        if generator is None:
            print("Choose a generation method:")
            print("\t1. Rule-based Pattern Matching")
            print("\t2. Sense-disambiguated Synonym Substitution")
            print("\t3. Zero-shot Machine Translation Model")
            print("\t4. Zero-shot Machine Translation Model (fine-tuned with reinforcement learning)")
            print("\t5. Easy Data Augmentation (EDA)")
            choice = int(input("> "))

            if choice == 1:
                generator = fpm
            elif choice == 2:
                generator = symsub
            # elif choice == 3:
            #     generator = imt
            elif choice == 3:
                generator = zeroshot
            elif choice == 4:
                generator = zeroshot_rl
            elif choice == 5:
                generator = eda
            else:
                print("Unknown option. Please try again.")
        else:
            input_sentence = input("Enter a sentence/question (enter 'menu' to select other method): ")

            if input_sentence == "menu":
                generator = None
            else:
                generated = generator.generate(input_sentence)

                print("\nGenerated questions:")
                for index, generation in enumerate(generated):
                    print(index + 1, generation)
                print('=' * 100)


if __name__ == '__main__':
    main()
