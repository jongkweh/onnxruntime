# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import unittest
import torch
import onnxruntime_pybind11_state as torch_ort

class OrtTensorTests(unittest.TestCase):
  def test_is_ort_via_alloc(self):
    cpu_ones = torch.zeros(10, 10)
    assert not cpu_ones.is_ort
    ort_ones = torch.zeros(10, 10, device='ort')
    assert ort_ones.is_ort
    assert torch.allclose(cpu_ones, ort_ones.cpu())

  def test_is_ort_via_to(self):
    cpu_ones = torch.ones(10, 10)
    assert not cpu_ones.is_ort
    ort_ones = cpu_ones.to('ort')
    assert ort_ones.is_ort
    assert torch.allclose(cpu_ones, ort_ones.cpu())

  def test_reshape(self):
    cpu_ones = torch.ones(10, 10)
    ort_ones = cpu_ones.to('ort')
    y = ort_ones.reshape(-1)
    assert len(y.size()) == 1
    assert y.size()[0] == 100

  def test_view(self):
    cpu_ones = torch.ones(2048)
    ort_ones = cpu_ones.to('ort')
    y = ort_ones.view(4, 512)
    assert y.size() == (4, 512)

  def test_view_neg1(self):
    cpu_ones = torch.ones(784, 256)
    ort_ones = cpu_ones.to('ort')
    y = ort_ones.view(-1)
    assert y.size()[0] == 200704

if __name__ == '__main__':
  unittest.main()