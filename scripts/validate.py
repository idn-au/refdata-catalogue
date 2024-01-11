import glob
from pathlib import Path
from pyshacl import validate


def validate_vocabs(vocab_files: list[str], validator: str):
    """Runs pySHACL validation on a list of files against a provided SHACL validator."""
    invalid_files = {}
    for file in vocab_files:
        v = validate(file, shacl_graph=validator, allow_infos=True, allow_warnings=True)
        file_name = file.split("/")[-1]
        print(f"{file_name} - {'Valid' if v[0] else 'Invalid'}")
        if not v[0]:
            invalid_files[file_name] = v[2]

        if len(invalid_files) > 0:
            print(
                "Invalid data:\n\n{}".format(
                    "\n\n".join(
                        [
                            f"{filename}\n{message}"
                            for filename, message in invalid_files.items()
                        ]
                    )
                )
            )
            raise ValueError(
                "\n\n{} invalid files: {}\n See above for details.".format(
                    len(invalid_files.keys()),
                    ", ".join([filename for filename in invalid_files.keys()]),
                )
            )


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    vocab_files = glob.glob(f"{project_root}/vocabs/*.ttl")
    validator_file_path = f"{project_root}/vocabs/validator/vocpub.ttl"
    with open(validator_file_path, "r") as validator_file:
        validator = validator_file.read()
    validate_vocabs(vocab_files, validator)
    print("validation complete")
