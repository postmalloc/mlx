import unittest
from itertools import permutations

import math
import mlx.core as mx
import numpy as np

import mlx_tests


class TestOps(mlx_tests.MLXTestCase):
    def test_full_ones_zeros(self):
        x = mx.full(2, 3.0)
        self.assertEqual(x.shape, [2])
        self.assertEqual(x.tolist(), [3.0, 3.0])

        x = mx.full((2, 3), 2.0)
        self.assertEqual(x.dtype, mx.float32)
        self.assertEqual(x.shape, [2, 3])
        self.assertEqual(x.tolist(), [[2, 2, 2], [2, 2, 2]])

        x = mx.full([3, 2], mx.array([False, True]))
        self.assertEqual(x.dtype, mx.bool_)
        self.assertEqual(x.tolist(), [[False, True], [False, True], [False, True]])

        x = mx.full([3, 2], mx.array([2.0, 3.0]))
        self.assertEqual(x.tolist(), [[2, 3], [2, 3], [2, 3]])

        x = mx.zeros(2)
        self.assertEqual(x.shape, [2])
        self.assertEqual(x.tolist(), [0.0, 0.0])

        x = mx.ones(2)
        self.assertEqual(x.shape, [2])
        self.assertEqual(x.tolist(), [1.0, 1.0])

        for t in [mx.bool_, mx.int32, mx.float32]:
            x = mx.zeros([2, 2], t)
            self.assertEqual(x.dtype, t)
            self.assertTrue(mx.array_equal(x, mx.array([[0, 0], [0, 0]])))
            y = mx.zeros_like(x)
            self.assertEqual(y.dtype, t)
            self.assertTrue(mx.array_equal(y, x))

            x = mx.ones([2, 2], t)
            self.assertEqual(x.dtype, t)
            self.assertTrue(mx.array_equal(x, mx.array([[1, 1], [1, 1]])))
            y = mx.ones_like(x)
            self.assertEqual(y.dtype, t)
            self.assertTrue(mx.array_equal(y, x))

    def test_scalar_inputs(self):
        # Check combinations of python types
        a = mx.add(False, True)
        self.assertEqual(a.dtype, mx.bool_)
        self.assertEqual(a.item(), True)

        a = mx.add(1, 2)
        self.assertEqual(a.dtype, mx.int32)
        self.assertEqual(a.item(), 3)

        a = mx.add(1.0, 2.0)
        self.assertEqual(a.dtype, mx.float32)
        self.assertEqual(a.item(), 3.0)

        a = mx.add(True, 2)
        self.assertEqual(a.dtype, mx.int32)
        self.assertEqual(a.item(), 3)

        a = mx.add(True, 2.0)
        self.assertEqual(a.dtype, mx.float32)
        self.assertEqual(a.item(), 3.0)

        a = mx.add(1, 2.0)
        self.assertEqual(a.dtype, mx.float32)
        self.assertEqual(a.item(), 3.0)

        a = mx.add(2, True)
        self.assertEqual(a.dtype, mx.int32)
        self.assertEqual(a.item(), 3)

        a = mx.add(2.0, True)
        self.assertEqual(a.dtype, mx.float32)
        self.assertEqual(a.item(), 3.0)

        a = mx.add(2.0, 1)
        self.assertEqual(a.dtype, mx.float32)
        self.assertEqual(a.item(), 3.0)

        # Check comibinations with mlx arrays
        a = mx.add(mx.array(True), False)
        self.assertEqual(a.dtype, mx.bool_)
        self.assertEqual(a.item(), True)

        a = mx.add(mx.array(1), False)
        self.assertEqual(a.dtype, mx.int32)
        self.assertEqual(a.item(), 1.0)

        # Edge case: take the type of the scalar
        a = mx.add(mx.array(True), 1)
        self.assertEqual(a.dtype, mx.int32)
        self.assertEqual(a.item(), 2)

        a = mx.add(mx.array(1.0), 1)
        self.assertEqual(a.dtype, mx.float32)
        self.assertEqual(a.item(), 2.0)

        a = mx.add(1, mx.array(1.0))
        self.assertEqual(a.dtype, mx.float32)
        self.assertEqual(a.item(), 2.0)

        binary_ops = [
            "add",
            "subtract",
            "multiply",
            "divide",
            "equal",
            "not_equal",
            "less",
            "greater",
            "less_equal",
            "greater_equal",
            "maximum",
            "minimum",
        ]

        for op in binary_ops:
            npop = getattr(np, op)
            mlxop = getattr(mx, op)

            # Avoid subtract from bool and divide by 0
            for x in [-1, 0, 1, -1.0, 1.0]:
                for y in [True, -1, 1, -1.0, 1.0]:
                    self.assertEqual(npop(x, y).item(), mlxop(x, y).item())

    def test_add(self):
        x = mx.array(1)
        y = mx.array(1)
        z = mx.add(x, y)
        self.assertEqual(z.item(), 2)

        x = mx.array(False, mx.bool_)
        z = x + 1
        self.assertEqual(z.dtype, mx.int32)
        self.assertEqual(z.item(), 1)
        z = 2 + x
        self.assertEqual(z.dtype, mx.int32)
        self.assertEqual(z.item(), 2)

        x = mx.array(1, mx.uint32)
        z = x + 3
        self.assertEqual(z.dtype, mx.uint32)
        self.assertEqual(z.item(), 4)

        z = 3 + x
        self.assertEqual(z.dtype, mx.uint32)
        self.assertEqual(z.item(), 4)

        z = x + 3.0
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 4.0)

        z = 3.0 + x
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 4.0)

        x = mx.array(1, mx.int64)
        z = x + 3
        self.assertEqual(z.dtype, mx.int64)
        self.assertEqual(z.item(), 4)
        z = 3 + x
        self.assertEqual(z.dtype, mx.int64)
        self.assertEqual(z.item(), 4)
        z = x + 3.0
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 4.0)
        z = 3.0 + x
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 4.0)

        x = mx.array(1, mx.float32)
        z = x + 3
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 4)
        z = 3 + x
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 4)

    def test_subtract(self):
        x = mx.array(4.0)
        y = mx.array(3.0)

        z = mx.subtract(x, y)
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 1.0)

        z = x - 3.0
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 1.0)

        z = 5.0 - x
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 1.0)

    def test_multiply(self):
        x = mx.array(2.0)
        y = mx.array(3.0)

        z = mx.multiply(x, y)
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 6.0)

        z = x * 3.0
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 6.0)

        z = 3.0 * x
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 6.0)

    def test_divide(self):
        x = mx.array(2.0)
        y = mx.array(4.0)

        z = mx.divide(x, y)
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 0.5)

        z = x / 4.0
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 0.5)

        z = 1.0 / x
        self.assertEqual(z.dtype, mx.float32)
        self.assertEqual(z.item(), 0.5)

    def test_comparisons(self):
        a = mx.array([0.0, 1.0, 5.0])
        b = mx.array([-1.0, 2.0, 5.0])

        self.assertEqual(mx.less(a, b).tolist(), [False, True, False])
        self.assertEqual(mx.less_equal(a, b).tolist(), [False, True, True])
        self.assertEqual(mx.greater(a, b).tolist(), [True, False, False])
        self.assertEqual(mx.greater_equal(a, b).tolist(), [True, False, True])

        self.assertEqual(mx.less(a, 5).tolist(), [True, True, False])
        self.assertEqual(mx.less(5, a).tolist(), [False, False, False])
        self.assertEqual(mx.less_equal(5, a).tolist(), [False, False, True])
        self.assertEqual(mx.greater(a, 1).tolist(), [False, False, True])
        self.assertEqual(mx.greater_equal(a, 1).tolist(), [False, True, True])

        a = mx.array([0.0, 1.0, 5.0, -1.0])
        b = mx.array([0.0, 2.0, 5.0, 3.0])
        self.assertEqual(mx.equal(a, b).tolist(), [True, False, True, False])
        self.assertEqual(mx.not_equal(a, b).tolist(), [False, True, False, True])

    def test_array_equal(self):
        x = mx.array([1, 2, 3, 4])
        y = mx.array([1, 2, 3, 4])
        self.assertTrue(mx.array_equal(x, y))

        y = mx.array([1, 2, 4, 5])
        self.assertFalse(mx.array_equal(x, y))

        y = mx.array([1, 2, 3])
        self.assertFalse(mx.array_equal(x, y))

        # Can still be equal with different types
        y = mx.array([1.0, 2.0, 3.0, 4.0])
        self.assertTrue(mx.array_equal(x, y))

        x = mx.array([0.0, float("nan")])
        y = mx.array([0.0, float("nan")])
        self.assertFalse(mx.array_equal(x, y))
        self.assertTrue(mx.array_equal(x, y, equal_nan=True))

        for t in [mx.float32, mx.float16, mx.bfloat16, mx.complex64]:
            with self.subTest(type=t):
                x = mx.array([0.0, float("nan")]).astype(t)
                y = mx.array([0.0, float("nan")]).astype(t)
                self.assertFalse(mx.array_equal(x, y))
                self.assertTrue(mx.array_equal(x, y, equal_nan=True))

    def test_minimum(self):
        x = mx.array([0.0, -5, 10.0])
        y = mx.array([1.0, -7.0, 3.0])

        expected = [0, -7, 3]
        self.assertListEqual(mx.minimum(x, y).tolist(), expected)

    def test_maximum(self):
        x = mx.array([0.0, -5, 10.0])
        y = mx.array([1.0, -7.0, 3.0])

        expected = [1, -5, 10]
        self.assertListEqual(mx.maximum(x, y).tolist(), expected)

    def test_transpose_noargs(self):
        x = mx.array([[0, 1, 1], [1, 0, 0]])

        expected = [
            [0, 1],
            [1, 0],
            [1, 0],
        ]

        self.assertListEqual(mx.transpose(x).tolist(), expected)

    def test_transpose_axis(self):
        x = mx.array(
            [
                [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]],
                [[12, 13, 14, 15], [16, 17, 18, 19], [20, 21, 22, 23]],
            ]
        )
        expected = [
            [[0, 4, 8], [1, 5, 9], [2, 6, 10], [3, 7, 11]],
            [[12, 16, 20], [13, 17, 21], [14, 18, 22], [15, 19, 23]],
        ]

        self.assertListEqual(mx.transpose(x, axes=(0, 2, 1)).tolist(), expected)

    def test_sum(self):
        x = mx.array(
            [
                [1, 2],
                [3, 3],
            ]
        )
        self.assertEqual(mx.sum(x).item(), 9)
        y = mx.sum(x, keepdims=True)
        self.assertEqual(y, mx.array(9))
        self.assertEqual(y.shape, [1, 1])

        self.assertEqual(mx.sum(x, axis=0).tolist(), [4, 5])
        self.assertEqual(mx.sum(x, axis=1).tolist(), [3, 6])

        x_npy = np.arange(3 * 5 * 4 * 7).astype(np.float32)
        x_npy = np.reshape(x_npy, (3, 5, 4, 7))
        x_mlx = mx.array(x_npy)

        for axis in (None, 0, 1, 2, 3, (0, 1), (2, 3), (1, 2, 3)):
            sum_npy = np.sum(x_npy, axis=axis)
            sum_mlx = np.asarray(mx.sum(x_mlx, axis=axis))
            self.assertListEqual(list(sum_npy.shape), list(sum_mlx.shape))
            self.assertTrue(np.all(sum_npy == sum_mlx))

        x_npy = np.array([1.0, 2.0, 3.0, 4.0]).astype(np.float32)
        x_mlx = mx.array(x_npy)

        y_npy = x_npy[0:4:2]
        y_npy = np.broadcast_to(y_npy, (2, 2))

        y_mlx = x_mlx[0:4:2]
        y_mlx = mx.broadcast_to(y_mlx, (2, 2))

        for axis in (None, 0, 1, (0, 1)):
            sum_npy = np.sum(y_npy, axis=axis)
            sum_mlx = np.asarray(mx.sum(y_mlx, axis=axis))
            self.assertListEqual(list(sum_npy.shape), list(sum_mlx.shape))
            self.assertTrue(np.all(sum_npy == sum_mlx))

    def test_prod(self):
        x = mx.array(
            [
                [1, 2],
                [3, 3],
            ]
        )
        self.assertEqual(mx.prod(x).item(), 18)
        y = mx.prod(x, keepdims=True)
        self.assertEqual(y, mx.array(18))
        self.assertEqual(y.shape, [1, 1])

        self.assertEqual(mx.prod(x, axis=0).tolist(), [3, 6])
        self.assertEqual(mx.prod(x, axis=1).tolist(), [2, 9])

    def test_min_and_max(self):
        x = mx.array(
            [
                [1, 2],
                [3, 4],
            ]
        )
        self.assertEqual(mx.min(x).item(), 1)
        self.assertEqual(mx.max(x).item(), 4)
        y = mx.min(x, keepdims=True)
        self.assertEqual(y.shape, [1, 1])
        self.assertEqual(y, mx.array(1))

        y = mx.max(x, keepdims=True)
        self.assertEqual(y.shape, [1, 1])
        self.assertEqual(y, mx.array(4))

        self.assertEqual(mx.min(x, axis=0).tolist(), [1, 2])
        self.assertEqual(mx.min(x, axis=1).tolist(), [1, 3])
        self.assertEqual(mx.max(x, axis=0).tolist(), [3, 4])
        self.assertEqual(mx.max(x, axis=1).tolist(), [2, 4])

    def test_argmin_argmax(self):
        data = np.random.rand(10, 12, 13)
        x = mx.array(data)
        for op in ["argmin", "argmax"]:
            for axis in range(3):
                for kd in [True, False]:
                    a = getattr(mx, op)(x, axis, kd)
                    b = getattr(np, op)(data, axis, keepdims=kd)
                    self.assertEqual(a.tolist(), b.tolist())

        for op in ["argmin", "argmax"]:
            a = getattr(mx, op)(x, keepdims=True)
            b = getattr(np, op)(data, keepdims=True)
            self.assertEqual(a.tolist(), b.tolist())
            a = getattr(mx, op)(x)
            b = getattr(np, op)(data)
            self.assertEqual(a.item(), b)

    def test_broadcast(self):
        a_npy = np.reshape(np.arange(200), (10, 20))
        a_mlx = mx.array(a_npy)

        b_npy = np.broadcast_to(a_npy, (30, 10, 20))
        b_mlx = mx.broadcast_to(a_mlx, (30, 10, 20))
        self.assertListEqual(list(b_npy.shape), list(b_mlx.shape))
        self.assertTrue(np.array_equal(b_npy, b_mlx))

        b_npy = np.broadcast_to(a_npy, (1, 10, 20))
        b_mlx = mx.broadcast_to(a_mlx, (1, 10, 20))
        self.assertListEqual(list(b_npy.shape), list(b_mlx.shape))
        self.assertTrue(np.array_equal(b_npy, b_mlx))

        b_npy = np.broadcast_to(1, (10, 20))
        b_mlx = mx.broadcast_to(1, (10, 20))
        self.assertListEqual(list(b_npy.shape), list(b_mlx.shape))
        self.assertTrue(np.array_equal(b_npy, b_mlx))

    def test_logsumexp(self):
        x = mx.array(
            [
                [1.0, 2.0],
                [3.0, 4.0],
            ]
        )
        xnp = np.array(x.tolist(), dtype=np.float32)
        expected = np.log(np.sum(np.exp(xnp)))
        self.assertTrue(math.isclose(mx.logsumexp(x).item(), expected.item()))

    def test_mean(self):
        x = mx.array(
            [
                [1, 2],
                [3, 4],
            ]
        )
        self.assertEqual(mx.mean(x).item(), 2.5)
        y = mx.mean(x, keepdims=True)
        self.assertEqual(y, mx.array(2.5))
        self.assertEqual(y.shape, [1, 1])

        self.assertEqual(mx.mean(x, axis=0).tolist(), [2, 3])
        self.assertEqual(mx.mean(x, axis=1).tolist(), [1.5, 3.5])

    def test_var(self):
        x = mx.array(
            [
                [1, 2],
                [3, 4],
            ]
        )
        self.assertEqual(mx.var(x).item(), 1.25)
        y = mx.var(x, keepdims=True)
        self.assertEqual(y, mx.array(1.25))
        self.assertEqual(y.shape, [1, 1])

        self.assertEqual(mx.var(x, axis=0).tolist(), [1.0, 1.0])
        self.assertEqual(mx.var(x, axis=1).tolist(), [0.25, 0.25])

    def test_abs(self):
        a = mx.array([-1.0, 1.0, -2.0, 3.0])
        result = mx.abs(a)
        expected = np.abs(a, dtype=np.float32)
        self.assertTrue(np.allclose(result, expected))

    def test_negative(self):
        a = mx.array([-1.0, 1.0, -2.0, 3.0])
        result = mx.negative(a)
        expected = np.negative(a, dtype=np.float32)
        self.assertTrue(np.allclose(result, expected))

    def test_sign(self):
        a = mx.array([-1.0, 1.0, 0.0, -2.0, 3.0])
        result = mx.sign(a)
        expected = np.sign(a, dtype=np.float32)
        self.assertTrue(np.allclose(result, expected))

    def test_logical_not(self):
        a = mx.array([-1.0, 1.0, 0.0, 1.0, -2.0, 3.0])
        result = mx.logical_not(a)
        expected = np.logical_not(a)
        self.assertTrue(np.array_equal(result, expected))

    def test_square(self):
        a = mx.array([0.1, 0.5, 1.0, 10.0])
        result = mx.square(a)
        expected = np.square(a, dtype=np.float32)

        self.assertTrue(np.allclose(result, expected))

    def test_sqrt(self):
        a = mx.array([0.1, 0.5, 1.0, 10.0])
        result = mx.sqrt(a)
        expected = np.sqrt(a, dtype=np.float32)
        self.assertTrue(np.allclose(result, expected))

    def test_rsqrt(self):
        a = mx.array([0.1, 0.5, 1.0, 10.0])
        result = mx.rsqrt(a)
        expected = 1.0 / np.sqrt(a, dtype=np.float32)
        self.assertTrue(np.allclose(result, expected))

    def test_reciprocal(self):
        a = mx.array([0.1, 0.5, 1.0, 2.0])
        result = mx.reciprocal(a)
        expected = np.reciprocal(a, dtype=np.float32)
        self.assertTrue(np.allclose(result, expected))

    def test_logaddexp(self):
        a = mx.array([0, 1, 2, 9.0])
        b = mx.array([1, 0, 4, 2.5])

        result = mx.logaddexp(a, b)
        expected = np.logaddexp(a, b, dtype=np.float32)

        self.assertTrue(np.allclose(result, expected))

    def test_log(self):
        a = mx.array([1, 0.5, 10, 100])
        result = mx.log(a)
        expected = np.log(a, dtype=np.float32)

        self.assertTrue(np.allclose(result, expected))

    def test_log2(self):
        a = mx.array([0.5, 1, 2, 10, 16])
        result = mx.log2(a)
        expected = np.log2(a, dtype=np.float32)

        self.assertTrue(np.allclose(result, expected))

    def test_log10(self):
        a = mx.array([0.1, 1, 10, 20, 100])
        result = mx.log10(a)
        expected = np.log10(a, dtype=np.float32)

        self.assertTrue(np.allclose(result, expected))

    def test_exp(self):
        a = mx.array([0, 0.5, -0.5, 5])
        result = mx.exp(a)
        expected = np.exp(a, dtype=np.float32)

        self.assertTrue(np.allclose(result, expected))

    def test_erf(self):
        inputs = [-5, 0.0, 0.5, 1.0, 2.0, 10.0]
        x = mx.array(inputs)
        expected = np.array([math.erf(i) for i in inputs])
        self.assertTrue(np.allclose(mx.erf(x), expected))

    def test_erfinv(self):
        inputs = [-5.0, -1.0, 0.5, 0.0, 0.5, 1.0, 5.0]
        x = mx.array(inputs)
        # Output of:
        # scipy.special.erfinv([-5.0, -1.0, 0.5, 0.0, 0.5, 1.0, 5.0])
        expected = np.array(
            [
                float("nan"),
                -float("inf"),
                0.47693628,
                0.0,
                0.47693628,
                float("inf"),
                float("nan"),
            ]
        ).astype(np.float32)
        self.assertTrue(np.allclose(mx.erfinv(x), expected, equal_nan=True))

    def test_sin(self):
        a = mx.array(
            [0, math.pi / 4, math.pi / 2, math.pi, 3 * math.pi / 4, 2 * math.pi]
        )
        result = mx.sin(a)
        expected = np.sin(a, dtype=np.float32)

        self.assertTrue(np.allclose(result, expected))

    def test_cos(self):
        a = mx.array(
            [0, math.pi / 4, math.pi / 2, math.pi, 3 * math.pi / 4, 2 * math.pi]
        )
        result = mx.cos(a)
        expected = np.cos(a, dtype=np.float32)

        self.assertTrue(np.allclose(result, expected))

    def test_log1p(self):
        a = mx.array([1, 0.5, 10, 100])
        result = mx.log1p(a)
        expected = np.log1p(a, dtype=np.float32)

        self.assertTrue(np.allclose(result, expected))

    def test_sigmoid(self):
        a = mx.array([0.0, 1.0, -1.0, 5.0, -5.0])
        result = mx.sigmoid(a)
        expected = 1 / (1 + np.exp(-a, dtype=np.float32))
        self.assertTrue(np.allclose(result, expected))

    def test_allclose(self):
        a = mx.array(1.0)
        b = mx.array(1.0)

        self.assertTrue(mx.allclose(a, b).item())

        b = mx.array(1.1)
        self.assertFalse(mx.allclose(a, b).item())
        self.assertTrue(mx.allclose(a, b, 0.1).item())
        self.assertFalse(mx.allclose(a, b, 0.01).item())
        self.assertTrue(mx.allclose(a, b, 0.01, 0.1).item())

    def test_all(self):
        a = mx.array([[True, False], [True, True]])

        self.assertFalse(mx.all(a).item())
        self.assertEqual(mx.all(a, keepdims=True).shape, [1, 1])
        self.assertFalse(mx.all(a, axis=[0, 1]).item())
        self.assertEqual(mx.all(a, axis=[0]).tolist(), [True, False])
        self.assertEqual(mx.all(a, axis=[1]).tolist(), [False, True])
        self.assertEqual(mx.all(a, axis=0).tolist(), [True, False])
        self.assertEqual(mx.all(a, axis=1).tolist(), [False, True])

    def test_any(self):
        a = mx.array([[True, False], [False, False]])

        self.assertTrue(mx.any(a).item())
        self.assertEqual(mx.any(a, keepdims=True).shape, [1, 1])
        self.assertTrue(mx.any(a, axis=[0, 1]).item())
        self.assertEqual(mx.any(a, axis=[0]).tolist(), [True, False])
        self.assertEqual(mx.any(a, axis=[1]).tolist(), [True, False])
        self.assertEqual(mx.any(a, axis=0).tolist(), [True, False])
        self.assertEqual(mx.any(a, axis=1).tolist(), [True, False])

    def test_stop_gradient(self):
        def func(x):
            return mx.sum(2 * x + mx.stop_gradient(3 * x))

        x = mx.array([0.0, 0.1, -3])
        expected = [2, 2, 2]

        self.assertListEqual(mx.grad(func)(x).tolist(), expected)

    def test_take(self):
        # Shape: 4 x 3 x 2
        l = [
            [[1, 3], [-2, -2], [-3, -2]],
            [[2, 4], [-3, 2], [-4, -2]],
            [[2, 3], [2, 4], [2, 1]],
            [[1, -5], [3, -1], [2, 3]],
        ]

        a = mx.array(l)
        a_npy = np.array(l)

        indices = [0, -1]
        flatten_take = mx.take(a, mx.array(indices)).tolist()
        flatten_take_expected = np.take(a_npy, np.array(indices)).tolist()
        self.assertListEqual(flatten_take, flatten_take_expected)

        indices = [-1, 2, 0]
        axis_take = mx.take(a, mx.array(indices), axis=0).tolist()
        axis_take_expected = np.take(a_npy, np.array(indices), axis=0).tolist()
        self.assertListEqual(axis_take, axis_take_expected)

        indices = [0, 0, -2]
        axis_take = mx.take(a, mx.array(indices), axis=1).tolist()
        axis_take_expected = np.take(a_npy, np.array(indices), axis=1).tolist()
        self.assertListEqual(axis_take, axis_take_expected)

        indices = [0, -1, -1]
        axis_take = mx.take(a, mx.array(indices), axis=-1).tolist()
        axis_take_expected = np.take(a_npy, np.array(indices), axis=-1).tolist()
        self.assertListEqual(axis_take, axis_take_expected)

        a_npy = np.arange(8 * 8 * 8, dtype=np.int32)
        a_npy = a_npy.reshape((8, 8, 8))
        idx_npy = np.arange(6, dtype=np.uint32)
        idx_npy = idx_npy.reshape((2, 3))
        a_mlx = mx.array(a_npy)
        idx_mlx = mx.array(idx_npy)

        a_npy_taken = np.take(a_npy, idx_npy)
        a_mlx_taken = mx.take(a_mlx, idx_mlx)
        self.assertListEqual(list(a_npy_taken.shape), a_mlx_taken.shape)
        self.assertListEqual(a_npy_taken.tolist(), a_mlx_taken.tolist())

        a_npy_taken = np.take(a_npy, idx_npy, axis=0)
        a_mlx_taken = mx.take(a_mlx, idx_mlx, axis=0)
        self.assertListEqual(list(a_npy_taken.shape), a_mlx_taken.shape)
        self.assertListEqual(a_npy_taken.tolist(), a_mlx_taken.tolist())

        a_npy_taken = np.take(a_npy, idx_npy, axis=1)
        a_mlx_taken = mx.take(a_mlx, idx_mlx, axis=1)
        self.assertListEqual(list(a_npy_taken.shape), a_mlx_taken.shape)
        self.assertListEqual(a_npy_taken.tolist(), a_mlx_taken.tolist())

        a_npy_taken = np.take(a_npy, idx_npy, axis=2)
        a_mlx_taken = mx.take(a_mlx, idx_mlx, axis=2)
        self.assertListEqual(list(a_npy_taken.shape), a_mlx_taken.shape)
        self.assertListEqual(a_npy_taken.tolist(), a_mlx_taken.tolist())

    def test_take_along_axis(self):
        a_np = np.arange(8).reshape(2, 2, 2)
        a_mlx = mx.array(a_np)
        idx_np = np.array([1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0])
        idx_mlx = mx.array(idx_np)

        for ax in [None, 0, 1, 2]:
            if ax == None:
                shape = [-1]
            else:
                shape = [2] * 3
                shape[ax] = 3
            out_np = np.take_along_axis(a_np, idx_np.reshape(shape), axis=ax)
            out_mlx = mx.take_along_axis(a_mlx, mx.reshape(idx_mlx, shape), axis=ax)
            self.assertTrue(np.array_equal(out_np, np.array(out_mlx)))

    def test_split(self):
        a = mx.array([1, 2, 3])
        splits = mx.split(a, 3)
        for e, x in enumerate(splits):
            self.assertEqual(x.item(), e + 1)

        a = mx.array([[1, 2], [3, 4], [5, 6]])
        x, y, z = mx.split(a, 3, axis=0)
        self.assertEqual(x.tolist(), [[1, 2]])
        self.assertEqual(y.tolist(), [[3, 4]])
        self.assertEqual(z.tolist(), [[5, 6]])

        a = mx.arange(8)
        x, y, z = mx.split(a, [1, 5])
        self.assertEqual(x.tolist(), [0])
        self.assertEqual(y.tolist(), [1, 2, 3, 4])
        self.assertEqual(z.tolist(), [5, 6, 7])

    def test_arange_overload_dispatch(self):
        a = mx.arange(5)
        expected = [0, 1, 2, 3, 4]
        self.assertListEqual(a.tolist(), expected)

        a = mx.arange(1, 5)
        expected = [1, 2, 3, 4]
        self.assertListEqual(a.tolist(), expected)

        a = mx.arange(-3, step=-1)
        expected = [0, -1, -2]
        self.assertListEqual(a.tolist(), expected)

        a = mx.arange(stop=2, step=0.5)
        expected = [0, 0.5, 1.0, 1.5]
        self.assertListEqual(a.tolist(), expected)

        with self.assertRaises(TypeError):
            mx.arange(start=1, step=2)

        a = mx.arange(stop=3)
        expected = [0, 1, 2]
        self.assertListEqual(a.tolist(), expected)

    def test_arange_inferred_dtype(self):
        a = mx.arange(5)
        self.assertEqual(a.dtype, mx.int32)

        a = mx.arange(5.0)
        self.assertEqual(a.dtype, mx.float32)

        a = mx.arange(1, 3.0)
        self.assertEqual(a.dtype, mx.float32)

        a = mx.arange(1, 3, dtype=mx.float32)
        self.assertEqual(a.dtype, mx.float32)

        a = mx.arange(1, 5, 1)
        self.assertEqual(a.dtype, mx.int32)

        a = mx.arange(1.0, 5, 1)
        self.assertEqual(a.dtype, mx.float32)

        a = mx.arange(1, 5.0, 1)
        self.assertEqual(a.dtype, mx.float32)

        a = mx.arange(1, 5, 1.0)
        self.assertEqual(a.dtype, mx.float32)

        a = mx.arange(1.0, 3.0, 0.2, dtype=mx.int32)
        self.assertEqual(a.dtype, mx.int32)

    def test_arange_corner_cases_cast(self):
        a = mx.arange(0, 3, 0.2, dtype=mx.int32)
        expected = [0] * 15
        self.assertListEqual(a.tolist(), expected)
        self.assertEqual(a.dtype, mx.int32)

        a = mx.arange(-1, -4, -0.9, dtype=mx.int32)
        expected = [-1] * 4
        self.assertListEqual(a.tolist(), expected)
        self.assertEqual(a.dtype, mx.int32)

        a = mx.arange(-1, -20, -1.2, dtype=mx.int32)
        expected = [
            -1,
            -2,
            -3,
            -4,
            -5,
            -6,
            -7,
            -8,
            -9,
            -10,
            -11,
            -12,
            -13,
            -14,
            -15,
            -16,
        ]
        self.assertListEqual(a.tolist(), expected)
        self.assertEqual(a.dtype, mx.int32)

    def test_unary_ops(self):
        def test_ops(npop, mlxop, x, y, atol):
            r_np = npop(x)
            r_mlx = mlxop(y)
            mx.eval(r_mlx)

            self.assertTrue(np.allclose(r_np, r_mlx, atol=atol))

        x = np.random.rand(18, 28, 38)
        for op in ["abs", "exp", "log", "square", "sqrt"]:
            with self.subTest(op=op):
                float_dtypes = [("float16", 1e-3), ("float32", 1e-6)]

                for dtype, atol in float_dtypes:
                    with self.subTest(dtype=dtype):
                        x_ = x.astype(getattr(np, dtype))
                        y_ = mx.array(x_)
                        test_ops(getattr(np, op), getattr(mx, op), x_, y_, atol)

    def test_trig_ops(self):
        def test_ops(npop, mlxop, x, y, atol):
            r_np = npop(x)
            r_mlx = mlxop(y)
            mx.eval(r_mlx)

            self.assertTrue(np.allclose(r_np, r_mlx, atol=atol))

        x = np.random.rand(9, 12, 18)
        xi = np.random.rand(9, 12, 18)
        base_ops = ["sin", "cos", "tan"]
        hyperbolic_ops = ["sinh", "cosh", "tanh"]
        all_fwd_ops = base_ops + hyperbolic_ops

        for op in all_fwd_ops:
            with self.subTest(op=op):
                float_dtypes = [("float16", 1e-3), ("float32", 1e-6)]

                for dtype, atol in float_dtypes:
                    with self.subTest(dtype=dtype):
                        x_ = x.astype(getattr(np, dtype))
                        y_ = mx.array(x_)
                        test_ops(getattr(np, op), getattr(mx, op), x_, y_, atol)

            with self.subTest(op=op):
                float_dtypes = [("complex64", 1e-5)]

                for dtype, atol in float_dtypes:
                    with self.subTest(dtype=dtype):
                        x_ = x + 1.0j * xi
                        x_ = x_.astype(getattr(np, dtype))
                        y_ = mx.array(x_)
                        test_ops(getattr(np, op), getattr(mx, op), x_, y_, atol)

            with self.subTest(op="arc" + op):
                float_dtypes = [("float16", 1e-3), ("float32", 1e-6)]
                op_inv = "arc" + op

                for dtype, atol in float_dtypes:
                    with self.subTest(dtype=dtype):
                        np_op_fwd = getattr(np, op)
                        x_ = np_op_fwd(x).astype(getattr(np, dtype))
                        y_ = mx.array(x_)
                        test_ops(getattr(np, op_inv), getattr(mx, op_inv), x_, y_, atol)

        # Test grads
        np_vjp_funcs = {
            "sin": lambda primal, cotan: cotan * np.cos(primal),
            "cos": lambda primal, cotan: -cotan * np.sin(primal),
            "tan": lambda primal, cotan: cotan / (np.cos(primal) ** 2),
            "sinh": lambda primal, cotan: cotan * np.cosh(primal),
            "cosh": lambda primal, cotan: cotan * np.sinh(primal),
            "tanh": lambda primal, cotan: cotan / (np.cosh(primal) ** 2),
            "arcsin": lambda primal, cotan: cotan / np.sqrt(1.0 - primal**2),
            "arccos": lambda primal, cotan: -cotan / np.sqrt(1.0 - primal**2),
            "arctan": lambda primal, cotan: cotan / (1.0 + primal**2),
            "arcsinh": lambda primal, cotan: cotan / np.sqrt(primal**2 + 1),
            "arccosh": lambda primal, cotan: cotan / np.sqrt(primal**2 - 1),
            "arctanh": lambda primal, cotan: cotan / (1.0 - primal**2),
        }
        with self.subTest(name="grads"):
            for op in all_fwd_ops:
                with self.subTest(op=op):
                    primal_np = xi.astype(np.float32)
                    primal_mx = mx.array(primal_np)
                    x_ = x.astype(np.float32)
                    y_ = mx.array(x_)
                    op_ = op
                    atol_ = 1e-5

                    np_vjp = lambda x: np_vjp_funcs[op_](primal_np, x)
                    mx_vjp = lambda x: mx.vjp(getattr(mx, op_), [primal_mx], [x])[1][0]
                    test_ops(np_vjp, mx_vjp, x_, y_, atol_)

                with self.subTest(op="arc" + op):
                    np_op_fwd = getattr(np, op)
                    primal_np = np_op_fwd(xi).astype(np.float32)

                    # To avoid divide by zero error
                    if op == "cosh":
                        primal_np[np.isclose(primal_np, 1.0)] += 1e-3
                    elif op == "cos":
                        primal_np[np.isclose(primal_np, 1.0)] -= 1e-3

                    primal_mx = mx.array(primal_np)
                    x_ = x.astype(np.float32)
                    y_ = mx.array(x_)
                    op_ = "arc" + op
                    atol_ = 1e-5

                    np_vjp = lambda x: np_vjp_funcs[op_](primal_np, x)
                    mx_vjp = lambda x: mx.vjp(getattr(mx, op_), [primal_mx], [x])[1][0]
                    test_ops(np_vjp, mx_vjp, x_, y_, atol_)

    def test_binary_ops(self):
        def test_ops(npop, mlxop, x, y, atol):
            r_np = npop(x, x)
            r_mlx = mlxop(y, y)
            mx.eval(r_mlx)
            self.assertTrue(np.allclose(r_np, r_mlx, atol=atol))

            r_np = npop(x[:1], x)
            r_mlx = mlxop(y[:1], y)
            mx.eval(r_mlx)
            self.assertTrue(np.allclose(r_np, r_mlx, atol=atol))

            r_np = npop(x[:, :1], x)
            r_mlx = mlxop(y[:, :1], y)
            mx.eval(r_mlx)
            self.assertTrue(np.allclose(r_np, r_mlx, atol=atol))

            r_np = npop(x[:, :, :1], x)
            r_mlx = mlxop(y[:, :, :1], y)
            mx.eval(r_mlx)
            self.assertTrue(np.allclose(r_np, r_mlx, atol=atol))

        x = np.maximum(np.random.rand(18, 28, 38), 0.1)
        y = mx.array(x)
        mx.eval(y)
        for op in [
            "add",
            "subtract",
            "multiply",
            "divide",
            "maximum",
            "minimum",
            "power",
        ]:
            with self.subTest(op=op):
                int_dtypes = [
                    "int8",
                    "int16",
                    "int32",
                    "int64",
                    "uint8",
                    "uint16",
                    "uint32",
                    "uint64",
                ]

                float_dtypes = ["float16", "float32"]

                dtypes = (
                    float_dtypes
                    if op in ("divide", "power")
                    else (int_dtypes + float_dtypes)
                )
                for dtype in dtypes:
                    atol = 1e-3 if dtype == "float16" else 1e-6
                    with self.subTest(dtype=dtype):
                        x_ = x.astype(getattr(np, dtype))
                        y_ = mx.array(x_)
                        test_ops(getattr(np, op), getattr(mx, op), x_, y_, atol)

    def test_irregular_binary_ops(self):
        # Check transposed binary ops
        dims = [2, 3, 4, 5]
        size = 3
        trial_mul = 2
        np.random.seed(0)
        for d in dims:
            anp = np.random.randint(-20, 20, (size**d,)).reshape([size] * d)
            bnp = np.random.randint(-20, 20, (size**d,)).reshape([size] * d)
            for _ in range(trial_mul * d):
                amlx = mx.array(anp)
                bmlx = mx.array(bnp)
                a_t = np.random.permutation(d).tolist()
                b_t = np.random.permutation(d).tolist()
                outnp = np.add(anp.transpose(a_t), bnp.transpose(b_t))
                outmlx = mx.add(mx.transpose(amlx, a_t), mx.transpose(bmlx, b_t))
                self.assertTrue(np.array_equal(outnp, outmlx))

        # Check broadcast binary ops
        for d in dims:
            anp = np.random.randint(-20, 20, (size**d,)).reshape([size] * d)
            for n_bsx in range(d):
                bnp = np.random.randint(-20, 20, (size**n_bsx,)).reshape(
                    [size] * n_bsx
                )
                for _ in range(trial_mul * d):
                    amlx = mx.array(anp)
                    bmlx = mx.array(bnp)
                    b_shape = [1] * (d - n_bsx) + [size] * n_bsx
                    np.random.shuffle(b_shape)
                    outnp = np.add(anp, bnp.reshape(b_shape))
                    outmlx = mx.add(amlx, mx.reshape(bmlx, b_shape))
                    self.assertTrue(np.array_equal(outnp, outmlx))

        # Check strided binary ops
        for d in dims:
            a = np.random.randint(-20, 20, (10,) * d)
            b = np.random.randint(-20, 20, (10,) * d)
            a_ = mx.array(a)
            b_ = mx.array(b)
            for t in permutations(range(d)):
                for s in range(d):
                    idx = tuple(
                        [slice(None)] * s
                        + [slice(None, None, 2)]
                        + [slice(None)] * (d - s - 1)
                    )
                    c = a.transpose(t)[idx] + b[idx]
                    c_ = mx.transpose(a_, t)[idx] + b_[idx]
                    self.assertTrue(np.array_equal(c, c_))

    def test_softmax(self):
        cases = [(np.float32, 1e-6), (np.float16, 1e-3)]

        for dtype, atol in cases:
            a_npy = np.random.randn(16, 8, 32).astype(dtype)
            a_mlx = mx.array(a_npy)

            def np_softmax(x, axis):
                ex = np.exp(x - np.max(x, axis=axis, keepdims=True))
                return ex / np.sum(ex, axis=axis, keepdims=True)

            for axes in (None, 0, 1, 2, (0, 1), (1, 2), (0, 2), (0, 1, 2)):
                b_npy = np_softmax(a_npy, axes)
                b_mlx = mx.softmax(a_mlx, axes)
                self.assertTrue(np.allclose(b_npy, b_mlx, atol=atol))

        for s in [100, 2049, 4097, 8193]:
            a = np.full(s, -np.inf)
            a[-1] = 0.0
            a = mx.softmax(mx.array(a))
            self.assertFalse(np.any(np.isnan(a)))
            self.assertTrue((a[:-1] == 0).all())
            self.assertEqual(a[-1], 1)

    def test_concatenate(self):
        a_npy = np.random.randn(32, 32, 32)
        b_npy = np.random.randn(32, 32, 32)
        a_mlx = mx.array(a_npy)
        b_mlx = mx.array(b_npy)

        for axis in (None, 0, 1, 2):
            for p in permutations([0, 1, 2]):
                c_npy = np.concatenate([a_npy, np.transpose(b_npy, p)], axis=axis)
                c_mlx = mx.concatenate([a_mlx, mx.transpose(b_mlx, p)], axis=axis)
                self.assertEqual(list(c_npy.shape), list(c_mlx.shape))
                self.assertTrue(np.allclose(c_npy, c_mlx, atol=1e-6))

    def test_pad(self):
        pad_width_and_values = [
            ([(1, 1), (1, 1), (1, 1)], 0),
            ([(1, 1), (1, 1), (1, 1)], 5),
            ([(3, 0), (0, 2), (5, 7)], 0),
            ([(3, 0), (0, 2), (5, 7)], -7),
            ([(0, 0), (0, 0), (0, 0)], 0),
        ]

        for pw, v in pad_width_and_values:
            with self.subTest(pad_width=pw, value=v):
                a_npy = np.random.randn(16, 16, 16).astype(np.float32)
                a_mlx = mx.array(a_npy)

                b_npy = np.pad(a_npy, pw, constant_values=v)
                b_mlx = mx.pad(a_mlx, pw, constant_values=v)

                self.assertEqual(list(b_npy.shape), list(b_mlx.shape))
                self.assertTrue(np.allclose(b_npy, b_mlx, atol=1e-6))

        a = mx.zeros((1, 1, 1))
        self.assertEqual(mx.pad(a, 1).shape, [3, 3, 3])
        self.assertEqual(mx.pad(a, (1,)).shape, [3, 3, 3])
        self.assertEqual(mx.pad(a, [1]).shape, [3, 3, 3])
        self.assertEqual(mx.pad(a, (1, 2)).shape, [4, 4, 4])
        self.assertEqual(mx.pad(a, [(1, 2)]).shape, [4, 4, 4])
        self.assertEqual(mx.pad(a, ((1, 2),)).shape, [4, 4, 4])
        self.assertEqual(mx.pad(a, ((1, 2), (2, 1), (2, 2))).shape, [4, 4, 5])

        # Test grads
        a_fwd = mx.array(np.random.rand(16, 16).astype(np.float32))
        a_bwd = mx.ones((22, 22))
        f = lambda x: mx.pad(x, ((4, 2), (2, 4)))

        _, df = mx.vjp(f, [a_fwd], [a_bwd])
        self.assertTrue(mx.allclose(a_bwd[4:-2, 2:-4], df[0]).item())

    def test_where(self):
        a = mx.array([[1, 2], [3, 4]])
        out = mx.where(True, a, 1)
        out_np = np.where(True, a, 1)
        self.assertTrue(np.array_equal(out, out_np))

        out = mx.where(True, 1, a)
        out_np = np.where(True, 1, a)
        self.assertTrue(np.array_equal(out, out_np))

        condition = mx.array([[True, False], [False, True]])
        b = mx.array([5, 6])
        out = mx.where(condition, a, b)
        out_np = np.where(condition, a, b)
        self.assertTrue(np.array_equal(out, out_np))

    def test_as_strided(self):
        x_npy = np.random.randn(128).astype(np.float32)
        x_mlx = mx.array(x_npy)

        shapes = [(10, 10), (5, 5), (2, 20), (10,)]
        strides = [(3, 3), (7, 1), (1, 5), (4,)]
        for shape, stride in zip(shapes, strides):
            for offset in [0, 1, 3]:
                y_npy = np.lib.stride_tricks.as_strided(
                    x_npy[offset:], shape, np.multiply(stride, 4)
                )
                y_mlx = mx.as_strided(x_mlx, shape, stride, offset)
                self.assertTrue(np.array_equal(y_npy, y_mlx))

    def test_scans(self):
        a_npy = np.random.randn(32, 32, 32).astype(np.float32)
        a_mlx = mx.array(a_npy)

        for op in ["cumsum", "cumprod"]:
            npop = getattr(np, op)
            mxop = getattr(mx, op)
            for axis in (None, 0, 1, 2):
                c_npy = npop(a_npy, axis=axis)
                c_mlx = mxop(a_mlx, axis=axis)
                self.assertTrue(np.allclose(c_npy, c_mlx, rtol=1e-4, atol=1e-4))

        for op in ["cumsum", "cumprod", "cummax", "cummin"]:
            c1 = mxop(a_mlx, axis=2)
            c2 = mxop(a_mlx, axis=2, inclusive=False, reverse=False)
            self.assertTrue(mx.array_equal(c1[:, :, :-1], c2[:, :, 1:]))
            c1 = mxop(a_mlx, axis=1)
            c2 = mxop(a_mlx, axis=1, inclusive=False, reverse=False)
            self.assertTrue(mx.array_equal(c1[:, :-1, :], c2[:, 1:, :]))
            c1 = mxop(a_mlx, axis=0)
            c2 = mxop(a_mlx, axis=0, inclusive=False, reverse=False)
            self.assertTrue(mx.array_equal(c1[:-1, :, :], c2[1:, :, :]))

            rev_idx = mx.arange(31, -1, -1)
            c1 = mxop(a_mlx[:, :, rev_idx], axis=2)[:, :, rev_idx]
            c2 = mxop(a_mlx, axis=2, inclusive=True, reverse=True)
            self.assertTrue(mx.array_equal(c1, c2))
            c1 = mxop(a_mlx[:, rev_idx, :], axis=1)[:, rev_idx, :]
            c2 = mxop(a_mlx, axis=1, inclusive=True, reverse=True)
            self.assertTrue(mx.array_equal(c1, c2))
            c1 = mxop(a_mlx[rev_idx, :, :], axis=0)[rev_idx, :, :]
            c2 = mxop(a_mlx, axis=0, inclusive=True, reverse=True)
            self.assertTrue(mx.array_equal(c1, c2))

            rev_idx = mx.arange(31, -1, -1)
            c1 = mxop(a_mlx[:, :, rev_idx], axis=2)[:, :, rev_idx][:, :, 1:]
            c2 = mxop(a_mlx, axis=2, inclusive=False, reverse=True)[:, :, :-1]
            self.assertTrue(mx.array_equal(c1, c2))
            c1 = mxop(a_mlx[:, rev_idx, :], axis=1)[:, rev_idx, :][:, 1:, :]
            c2 = mxop(a_mlx, axis=1, inclusive=False, reverse=True)[:, :-1, :]
            self.assertTrue(mx.array_equal(c1, c2))
            c1 = mxop(a_mlx[rev_idx, :, :], axis=0)[rev_idx, :, :][1:, :, :]
            c2 = mxop(a_mlx, axis=0, inclusive=False, reverse=True)[:-1, :, :]
            self.assertTrue(mx.array_equal(c1, c2))

    def test_squeeze_expand(self):
        a = mx.zeros((2, 1, 2, 1))
        self.assertEqual(mx.squeeze(a).shape, [2, 2])
        self.assertEqual(mx.squeeze(a, 1).shape, [2, 2, 1])
        self.assertEqual(mx.squeeze(a, [1, 3]).shape, [2, 2])
        self.assertEqual(a.squeeze().shape, [2, 2])
        self.assertEqual(a.squeeze(1).shape, [2, 2, 1])
        self.assertEqual(a.squeeze([1, 3]).shape, [2, 2])

        a = mx.zeros((2, 2))
        self.assertEqual(mx.squeeze(a).shape, [2, 2])

        self.assertEqual(mx.expand_dims(a, 0).shape, [1, 2, 2])
        self.assertEqual(mx.expand_dims(a, (0, 1)).shape, [1, 1, 2, 2])
        self.assertEqual(mx.expand_dims(a, [0, -1]).shape, [1, 2, 2, 1])

    def test_sort(self):
        shape = (3, 4, 5)
        for dtype in ("int32", "float32"):
            for axis in (None, 0, 1, 2):
                with self.subTest(dtype=dtype, axis=axis):
                    np.random.seed(0)
                    np_dtype = getattr(np, dtype)
                    a_np = np.random.uniform(0, 100, size=shape).astype(np_dtype)
                    a_mx = mx.array(a_np)

                    b_np = np.sort(a_np, axis=axis)
                    b_mx = mx.sort(a_mx, axis=axis)

                    self.assertTrue(np.array_equal(b_np, b_mx))
                    self.assertEqual(b_mx.dtype, a_mx.dtype)

                    c_np = np.argsort(a_np, axis=axis)
                    c_mx = mx.argsort(a_mx, axis=axis)
                    d_np = np.take_along_axis(a_np, c_np, axis=axis)
                    d_mx = mx.take_along_axis(a_mx, c_mx, axis=axis)

                    self.assertTrue(np.array_equal(d_np, d_mx))
                    self.assertEqual(c_mx.dtype, mx.uint32)

    def test_partition(self):
        shape = (3, 4, 5)
        for dtype in ("int32", "float32"):
            for axis in (None, 0, 1, 2):
                for kth in (-2, 2):
                    with self.subTest(dtype=dtype, axis=axis, kth=kth):
                        np.random.seed(0)
                        np_dtype = getattr(np, dtype)
                        a_np = np.random.uniform(0, 100, size=shape).astype(np_dtype)
                        a_mx = mx.array(a_np)

                        b_np = np.partition(a_np, kth, axis=axis)
                        b_mx = mx.partition(a_mx, kth, axis=axis)

                        c_np = np.take(b_np, (kth,), axis=axis)
                        c_mx = np.take(np.array(b_mx), (kth,), axis=axis)

                        self.assertTrue(np.array_equal(c_np, c_mx))
                        self.assertEqual(b_mx.dtype, a_mx.dtype)

                        top_k_mx = mx.topk(a_mx, kth, axis=axis)
                        self.assertTrue(np.all(c_np <= top_k_mx))
                        self.assertEqual(top_k_mx.dtype, a_mx.dtype)

                        if kth >= 0:
                            d_np = np.take(b_mx, np.arange(kth), axis=axis)
                            self.assertTrue(np.all(d_np <= c_mx))


if __name__ == "__main__":
    unittest.main()