import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';

// Mock fetch
global.fetch = vi.fn();

describe('App Component', () => {
  it('renders correctly and handles search', async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        query: 'BRCA1',
        pdb_result: {
          entry_id: '1XYZ',
          title: 'Test Protein',
          deposition_date: null,
          release_date: null,
          resolution_combined: [1.5],
          experimental_method: ['X-RAY DIFFRACTION'],
          polymer_entity_count: 1,
          molecular_weight: 50000.0,
        },
        ncbi_result: {
          gene_id: '1234',
          name: 'BRCA1',
          description: 'BRCA1 DNA repair associated',
          organism: 'Homo sapiens'
        }
      })
    });

    render(<App />);

    // Check title
    expect(screen.getByText('BioInfo Nexus')).toBeDefined();

    // Find input and type
    const input = screen.getByPlaceholderText(/Enter Gene or PDB ID/i);
    fireEvent.change(input, { target: { value: 'BRCA1' } });
    
    // Click search
    const button = screen.getByRole('button');
    fireEvent.click(button);

    // Wait for the data to load and render
    await waitFor(() => {
      expect(screen.getByText('Test Protein')).toBeDefined();
      expect(screen.getByText('BRCA1 DNA repair associated')).toBeDefined();
    });
  });
});
