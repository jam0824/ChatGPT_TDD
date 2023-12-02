import sys
from ModuleConvertTop import ConvertTop

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    result = ConvertTop().process_file(file_name)

    labels = ["time", "up_time", "CPU(user)", "CPU(system)", "CPU(ni)", "Mem(%)"]
    print(",".join(labels))
    print(result)

if __name__ == "__main__":
    main()