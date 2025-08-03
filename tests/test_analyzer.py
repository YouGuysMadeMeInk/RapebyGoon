import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import the analyzer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analyze_behavior import TurtleBehaviorAnalyzer

class TestTurtleBehaviorAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.analyzer = TurtleBehaviorAnalyzer(species='test_species', duration='1h')
        
    def test_initialization(self):
        """Test that the analyzer initializes with correct parameters."""
        self.assertEqual(self.analyzer.species, 'test_species')
        self.assertEqual(self.analyzer.duration, '1h')
        self.assertEqual(self.analyzer.data_points, [])
        self.assertEqual(self.analyzer.analysis_results, {})
    
    def test_synthetic_data_generation(self):
        """Test synthetic data generation functionality."""
        self.analyzer._generate_synthetic_data()
        
        # Check that tracking_data is created
        self.assertIsNotNone(self.analyzer.tracking_data)
        self.assertIsInstance(self.analyzer.tracking_data, pd.DataFrame)
        
        # Check expected columns
        expected_columns = ['timestamp', 'turtle_id', 'x_position', 'y_position', 'velocity', 'interaction_type']
        for col in expected_columns:
            self.assertIn(col, self.analyzer.tracking_data.columns)
        
        # Check data types and ranges
        self.assertTrue(len(self.analyzer.tracking_data) > 0)
        self.assertTrue(all(self.analyzer.tracking_data['velocity'] >= 0))
    
    @patch('pandas.read_csv')
    def test_load_data_success(self, mock_read_csv):
        """Test successful data loading from CSV file."""
        # Mock the CSV data
        mock_data = pd.DataFrame({
            'timestamp': pd.date_range(start='2024-01-01', periods=5, freq='1min'),
            'turtle_id': ['turtle_a'] * 5,
            'x_position': [1, 2, 3, 4, 5],
            'y_position': [1, 2, 3, 4, 5],
            'velocity': [0.1, 0.2, 0.3, 0.4, 0.5],
            'interaction_type': ['neutral'] * 5
        })
        mock_read_csv.return_value = mock_data
        
        self.analyzer.load_data('test_path.csv')
        
        mock_read_csv.assert_called_once_with('test_path.csv')
        pd.testing.assert_frame_equal(self.analyzer.tracking_data, mock_data)
    
    @patch('pandas.read_csv')
    def test_load_data_file_not_found(self, mock_read_csv):
        """Test handling of missing data file."""
        mock_read_csv.side_effect = FileNotFoundError("File not found")
        
        with patch.object(self.analyzer, '_generate_synthetic_data') as mock_generate:
            self.analyzer.load_data('nonexistent_file.csv')
            mock_generate.assert_called_once()
    
    def test_movement_analysis(self):
        """Test movement pattern analysis functionality."""
        # Set up test data
        self.analyzer._generate_synthetic_data()
        
        # Run analysis
        self.analyzer.analyze_movement_patterns()
        
        # Check that results were generated
        self.assertIn('avg_distance', self.analyzer.analysis_results)
        self.assertIn('min_distance', self.analyzer.analysis_results)
        self.assertIn('interaction_frequency', self.analyzer.analysis_results)
        
        # Verify result types and ranges
        self.assertIsInstance(self.analyzer.analysis_results['avg_distance'], (int, float))
        self.assertIsInstance(self.analyzer.analysis_results['min_distance'], (int, float))
        self.assertIsInstance(self.analyzer.analysis_results['interaction_frequency'], int)
        
        self.assertGreaterEqual(self.analyzer.analysis_results['min_distance'], 0)
        self.assertGreaterEqual(self.analyzer.analysis_results['interaction_frequency'], 0)
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.subplots')
    def test_visualization_generation(self, mock_subplots, mock_savefig):
        """Test visualization generation."""
        # Mock matplotlib components
        mock_fig = MagicMock()
        mock_axes = np.array([[MagicMock(), MagicMock()], [MagicMock(), MagicMock()]])
        mock_subplots.return_value = (mock_fig, mock_axes)
        
        # Set up test data
        self.analyzer._generate_synthetic_data()
        self.analyzer.analyze_movement_patterns()
        
        # Generate visualizations
        self.analyzer.generate_visualizations()
        
        # Verify that matplotlib functions were called
        mock_subplots.assert_called_once()
        mock_savefig.assert_called_once()
    
    @patch('pandas.DataFrame.to_csv')
    def test_export_results(self, mock_to_csv):
        """Test results export functionality."""
        # Set up test data and run analysis
        self.analyzer._generate_synthetic_data()
        self.analyzer.analyze_movement_patterns()
        
        # Export results
        self.analyzer.export_results()
        
        # Verify CSV export was called
        mock_to_csv.assert_called_once()
        args, kwargs = mock_to_csv.call_args
        self.assertIn('analysis_results_', args[0])
        self.assertEqual(kwargs['index'], False)

if __name__ == '__main__':
    unittest.main()
