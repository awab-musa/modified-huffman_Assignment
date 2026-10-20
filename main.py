from compress_decompress import compress, decompress


def main():
    print("1) Compress")
    print("2) Decompress")
    choice = input("Choose (1/2): ")
    if choice == "1":
        in_path = input("Input file: ")
        out_path = input("Output file: ")
        p_min = float(input("Minimum probability p_min (e.g. 0.01): "))
        compress(in_path, out_path, p_min)
    elif choice == "2":
        in_path = input("Compressed file: ")
        out_path = input("Output file: ")
        decompress(in_path, out_path)
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()