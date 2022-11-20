# Distributed Minimum Spanning Tree using the GHS Algorithm

## Usage

```sh
git clone https://github.com/Aditya-Harikrish/Distributed-MST.git
cd Distributed-MST
mpiexec -n <num_processes> python3 src/main.py <path_to_input_file_ending_with_.in>
```

To convert a Matrix Market file (file extension: .mtx) into the desired format that ends with .in, do the following:
```
python3 src/GenerateInput.py <file_path.mtx>
```
The output goes to file_path.in. See [GenerateInput.py](https://github.com/Aditya-Harikrish/Distributed-MST/blob/main/src/GenerateInput.py) for more details.