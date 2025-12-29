# GPU Acceleration Setup

This bot can optionally use an NVIDIA GPU to accelerate certain operations. Follow these steps:

1. **Install Drivers**: Install the latest drivers for your NVIDIA GPU.
2. **Install CUDA Toolkit 11.8**: [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-11-8-0-download-archive)
3. **Install cuDNN v8.6.0 (October 3rd, 2022) for CUDA 11.x**:
   * Download the ZIP folder from [NVIDIA cuDNN Archive](https://developer.nvidia.com/rdp/cudnn-archive)
4. **Extract and Move Files**:
   Extract the ZIP and move its contents to the respective CUDA folders. For example:
   
   Move contents from:
   `cudnn-windows-x86_64-8.6.0.163_cuda11-archive\bin`
   
   To:
   `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin`

   **Repeat this for all folders (include, lib, etc.) inside the archive.**

5. **Update System PATH**:
   Add the following three folders to your system **PATH** environment variable:
   * `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin`
   * `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\libnvvp`
   * `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8`

6. **Fix Missing DLL**:
   Copy this file:
   `C:\Program Files\NVIDIA Corporation\Nsight Systems 2022.4.2\host-windows-x64\zlib.dll`
   
   Paste it into:
   `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin`
   
   **Rename it to `zlibwapi.dll`.**

7. **Reinstall PaddlePaddle for GPU**:
   Uninstall the CPU version:
   ```bash
   pip uninstall paddlepaddle
   ```
   
   Install the GPU version:
   ```bash
   pip install paddlepaddle-gpu==2.6.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

8. **Update Requirements**:
   Open `requirements.txt` and change line 71 from:
   ```text
   paddlepaddle==2.6.2
   ```
   to:
   ```text
   paddlepaddle-gpu==2.6.2
   ```

9. **Reboot**: Restart your computer.