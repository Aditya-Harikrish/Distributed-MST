# Distributed Minimum Spanning Tree using the GHS Algorithm

## Usage

```sh
git clone https://github.com/Aditya-Harikrish/Distributed-MST.git
cd Distributed-MST
mpiexec -n <num_processes> python3 src/main.py <path_to_input_file_ending_with_.in>
```

To convert a Matrix Market file (file extension: .mtx) into the desired format that ends with .in, do the following:
```
python3 src/ConvertInputFormat.py <path_to_input_file_ending_with_.mtx> <indexing>
```
where &lt;indexing&gt; (0, 1, 2,...) is the base of indexing of the vertices. Usually, it's either 0 or 1. 

The output goes to file_path.in. See [GenerateInput.py](https://github.com/Aditya-Harikrish/Distributed-MST/blob/main/src/GenerateInput.py) for more details.

