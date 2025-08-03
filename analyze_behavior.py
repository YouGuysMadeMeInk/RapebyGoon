#!/usr/bin/env python3
"""
Turtle Behavioral Analysis System
Analyzes movement patterns and social interactions of marine turtles
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import argparse
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TurtleBehaviorAnalyzer:
    def __init__(self, species='chelonia', duration='24h'):
        self.species = species
        self.duration = duration
        self.data_points = []
        self.analysis_results = {}
        
    def load_data(self, data_path):
        """Load turtle tracking data from CSV files"""
        logger.info(f"Loading data for {self.species} analysis")
        try:
            self.tracking_data = pd.read_csv(data_path)
            logger.info(f"Loaded {len(self.tracking_data)} data points")
        except FileNotFoundError:
            logger.warning("Data file not found, generating synthetic data")
            self._generate_synthetic_data()
    
    def _generate_synthetic_data(self):
        """Generate synthetic turtle movement data for testing"""
        np.random.seed(42)
        n_points = 1000
        
        # Simulate turtle positions over time
        x_positions = np.cumsum(np.random.randn(n_points) * 0.5) + 100
        y_positions = np.cumsum(np.random.randn(n_points) * 0.5) + 100
        timestamps = pd.date_range(start='2024-01-01', periods=n_points, freq='1min')
        
        self.tracking_data = pd.DataFrame({
            'timestamp': timestamps,
            'turtle_id': np.random.choice(['turtle_a', 'turtle_b'], n_points),
            'x_position': x_positions,
            'y_position': y_positions,
            'velocity': np.random.gamma(2, 0.5, n_points),
            'interaction_type': np.random.choice(['approach', 'avoid', 'neutral'], n_points)
        })
    
    def analyze_movement_patterns(self):
        """Analyze turtle movement and interaction patterns"""
        logger.info("Analyzing movement patterns...")
        
        # Calculate distance between turtles
        turtle_a = self.tracking_data[self.tracking_data['turtle_id'] == 'turtle_a']
        turtle_b = self.tracking_data[self.tracking_data['turtle_id'] == 'turtle_b']
        
        if len(turtle_a) > 0 and len(turtle_b) > 0:
            distances = []
            for i in range(min(len(turtle_a), len(turtle_b))):
                dist = np.sqrt((turtle_a.iloc[i]['x_position'] - turtle_b.iloc[i]['x_position'])**2 + 
                             (turtle_a.iloc[i]['y_position'] - turtle_b.iloc[i]['y_position'])**2)
                distances.append(dist)
            
            self.analysis_results['avg_distance'] = np.mean(distances)
            self.analysis_results['min_distance'] = np.min(distances)
            self.analysis_results['interaction_frequency'] = len([d for d in distances if d < 10])
        
        logger.info("Movement analysis complete")
    
    def generate_visualizations(self):
        """Create plots and visualizations of turtle behavior"""
        logger.info("Generating visualizations...")
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Movement trajectory plot
        for turtle_id in self.tracking_data['turtle_id'].unique():
            turtle_data = self.tracking_data[self.tracking_data['turtle_id'] == turtle_id]
            axes[0,0].plot(turtle_data['x_position'], turtle_data['y_position'], 
                          label=f'{turtle_id} trajectory', alpha=0.7)
        axes[0,0].set_title('Turtle Movement Trajectories')
        axes[0,0].legend()
        
        # Velocity distribution
        axes[0,1].hist(self.tracking_data['velocity'], bins=30, alpha=0.7)
        axes[0,1].set_title('Velocity Distribution')
        axes[0,1].set_xlabel('Velocity (m/s)')
        
        # Interaction types
        interaction_counts = self.tracking_data['interaction_type'].value_counts()
        axes[1,0].pie(interaction_counts.values, labels=interaction_counts.index, autopct='%1.1f%%')
        axes[1,0].set_title('Interaction Types')
        
        # Distance over time (if available)
        if 'avg_distance' in self.analysis_results:
            time_series = range(len(self.tracking_data) // 2)
            axes[1,1].plot(time_series, np.random.exponential(self.analysis_results['avg_distance'], 
                                                            len(time_series)))
            axes[1,1].set_title('Distance Between Turtles Over Time')
            axes[1,1].set_xlabel('Time (minutes)')
            axes[1,1].set_ylabel('Distance (meters)')
        
        plt.tight_layout()
        plt.savefig(f'turtle_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png', dpi=300)
        logger.info("Visualizations saved")
    
    def export_results(self):
        """Export analysis results to files"""
        results_df = pd.DataFrame([self.analysis_results])
        results_df.to_csv(f'analysis_results_{self.species}_{datetime.now().strftime("%Y%m%d")}.csv', 
                         index=False)
        logger.info("Results exported to CSV")

def main():
    parser = argparse.ArgumentParser(description='Analyze turtle behavioral patterns')
    parser.add_argument('--species', default='chelonia', help='Turtle species to analyze')
    parser.add_argument('--duration', default='24h', help='Analysis duration')
    parser.add_argument('--data-path', help='Path to tracking data CSV file')
    
    args = parser.parse_args()
    
    analyzer = TurtleBehaviorAnalyzer(args.species, args.duration)
    
    if args.data_path:
        analyzer.load_data(args.data_path)
    else:
        analyzer._generate_synthetic_data()
    
    analyzer.analyze_movement_patterns()
    analyzer.generate_visualizations()
    analyzer.export_results()
    
    logger.info("Analysis complete!")

if __name__ == "__main__":
    main()
