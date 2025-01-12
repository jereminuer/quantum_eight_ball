####### IMPORTS ########
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.providers.basic_provider import BasicSimulator
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2 as Sampler

import math

class UniformDistributionCircuit:
   """
   A quantum circuit that produces uniformly distributed random integers in the
   range [0, num_range-1].
   """


   def __init__(self, num_range: int, token: str = None):
      """
      :param num_range: The upper bound (exclusive) for the random numbers generated 
      :raises ValueError: If num_range <= 1
      :raises TypeError: If num_range is not an int
      """

      # Type Check and Value Check
      if not isinstance(num_range, int):
         raise TypeError("Argument 'num_range' must be an integer")
      if num_range <= 1:
         raise ValueError("Our range must be greater than 1 for a meaningful distribution")

      # Initialize simulator, range of distribution, and IBM Quantum Token
      self.simulator = BasicSimulator()
      self.range = num_range
      self.token = token

      # Determine amount of qubits needed
      qbts = math.ceil(math.log2(num_range))

      # Define our Quantum Register and quantum circuit
      q_circuit = QuantumRegister(qbts)
      self.circuit = QuantumCircuit(q_circuit)

      # Set H gates for all qubits, and add measurements for those qubits
      for qbit in range(qbts):
         self.circuit.reset(qbit)
         self.circuit.h(qbit)
      self.circuit.measure_all()
   

   def __run_simulator(self):
      """
      A wrapper over IBM quantum simulator which will run one measurement,
      and convert the binary value (combination of qubits) to an integer value
      :returns int: sampled value
      """

      #Run one shot job
      job = self.simulator.run(self.circuit, shots=1, memory=True)
      result = job.result()
      samples = result.get_memory()
      #Translate binary to int
      return int(samples[0], 2)
   

   def __run_QPU(self):
      """
      Connects to IBM Quantum Computer and runs measurement of given circuit
      on physical QPU. 
      """

      # 1. Connect to Qiskit Runtime Service
      try:
         service = QiskitRuntimeService(
            token=self.token, 
            channel="ibm_quantum"
            )
      except Exception as e:
         raise RuntimeError(f"Failed to initialize QiskitRuntimeService: {e}")
      
      # 2. Find a suitable backend
      try:
         backend = service.least_busy(simulator=False, operational=True)
      except Exception as e:
         raise RuntimeError(f"Failed to find a backend (physical QPU): {e}")
      
      # 3. Translate to ISA architecture
      try:
         pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
         isa_circuit = pm.run(self.circuit)
      except Exception as e:
         raise RuntimeError(f"Failed to convert to ISA architecture: {e}")

      # Initialize sampler
      try:
         sampler = Sampler(mode=backend)
      except Exception as e:
         raise RuntimeError(f"Failed to initialize sampler: {e}")

      # 4. Run circuit on selected backend
      try:
         result = sampler.run([isa_circuit], shots=1000).result()
         # extract array from databin from result
         databin = result[0].data
         bitarray = databin.meas
         return bitarray.array

      except Exception as e:
         raise RuntimeError(f"Job failed to execute: {e}")


   def measure(self, sample_type="sim", max_attempts=1000):
      """
      Measures value either from simulator or from actual QPU, and restricts within range.
      :param sample_type (optional): "sim" if running on simulator, "QPU" if not
      returns int: sampled value WITHIN given uniform distribution
      """

      if sample_type != "sim" and self.token == None:
         raise ValueError("""If running on QPU, please initialize UniformDistributionCircuit with your IBM token. 
                          If you didn't mean to run on QPU, ensure that sample_type = 'sim'. """)
      attempts = 0
      # Run one measurement (either on simulator or physical QPU)
      values = self.__run_simulator() if sample_type == "sim" else self.__run_QPU()

      # IF ON SIMULATOR: Keep running measurements until number is within desired range
      if sample_type == "sim":
         while values > self.range - 1:
            attempts += 1
            values = value = self.__run_simulator() if sample_type == "sim" else self.__run_QPU()
            if attempts > max_attempts:
               raise RuntimeError("Too many out of range samples. Check the circuit is configured correctly")
         return values
      
      # IF ON PHYSICAL QPU: run 1000 shots, iterate through each shot until we find a value within desired range
      else:
         for val in values:
            if val[0] < 20:
               return val[0]
