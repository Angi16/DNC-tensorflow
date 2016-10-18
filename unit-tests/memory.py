import tensorflow as tf
import numpy as np
import unittest

from dnc.memory import Memory

class DNCMemoryTests(unittest.TestCase):

    def test_construction(self):
        graph = tf.Graph()
        with graph.as_default():
            with tf.Session(graph=graph) as session:

                mem = Memory(4, 5, 2)
                session.run(tf.initialize_all_variables())

                self.assertEqual(mem.words_num, 4)
                self.assertEqual(mem.word_size, 5)
                self.assertEqual(mem.read_heads, 2)

                self.assertTrue(isinstance(mem.memory_matrix, tf.Variable))
                self.assertEqual(mem.memory_matrix.get_shape().as_list(), [4, 5])
                self.assertTrue(isinstance(mem.usage_vector, tf.Variable))
                self.assertEqual(mem.usage_vector.get_shape().as_list(), [4])
                self.assertTrue(isinstance(mem.link_matrix, tf.Variable))
                self.assertEqual(mem.link_matrix.get_shape().as_list(), [4, 4])
                self.assertTrue(isinstance(mem.write_weighting, tf.Variable))
                self.assertEqual(mem.write_weighting.get_shape().as_list(), [4])
                self.assertTrue(isinstance(mem.read_weightings, tf.Variable))
                self.assertEqual(mem.read_weightings.get_shape().as_list(), [2, 4])
                self.assertTrue(isinstance(mem.read_vectors, tf.Variable))
                self.assertEqual(mem.read_vectors.get_shape().as_list(), [2, 5])


    def test_lookup_weighting(self):
        graph = tf.Graph()
        with graph.as_default():
            with tf.Session(graph=graph) as session:

                mem = Memory(4, 5, 2)
                keys = np.array([[0., 1., 0., 0.3, 4.3], [1.3, 0.8, 0., 0., 0.62]]).astype(np.float32)
                strengths = np.array([0.7, 0.2]).astype(np.float32)
                predicted_weights = np.array([[0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.25, 0.25]]).astype(np.float32)

                op = mem.get_lookup_weighting(keys, strengths)
                session.run(tf.initialize_all_variables())
                c = session.run(op)

                self.assertTrue(c.shape, (2, 4))
                self.assertTrue(np.array_equal(c, predicted_weights))

if __name__ == '__main__':
    unittest.main(verbosity=2)
