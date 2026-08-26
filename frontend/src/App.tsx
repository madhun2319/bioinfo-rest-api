import { useState } from 'react';
import { Search, Loader2, Database, Dna, AlertCircle } from 'lucide-react';

interface PdbResult {
  entry_id: string;
  title: string | null;
  deposition_date: string | null;
  release_date: string | null;
  resolution_combined: number[] | null;
  experimental_method: string[] | null;
  polymer_entity_count: number | null;
  molecular_weight: number | null;
}

interface NcbiResult {
  gene_id: string;
  name: string | null;
  description: string | null;
  organism: string | null;
}

interface UniprotResult {
  primary_accession: string;
  protein_name: string | null;
  organism: string | null;
  sequence_length: number | null;
}

interface ServiceResponse<T> {
  status: 'success' | 'not_found' | 'error';
  data: T | null;
  error_message: string | null;
}

interface AggregateResponse {
  query: string;
  pdb_result: ServiceResponse<PdbResult>;
  ncbi_result: ServiceResponse<NcbiResult>;
  uniprot_result: ServiceResponse<UniprotResult>;
}

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AggregateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const baseUrl = import.meta.env.VITE_API_URL || '';
      const response = await fetch(`${baseUrl}/api/aggregate?term=${encodeURIComponent(query)}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch data from API');
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen">
      <div className="background-mesh" />
      
      <div className="container mx-auto px-4 py-16 flex flex-col items-center">
        <header className="text-center mb-12">
          <h1 className="text-5xl md:text-6xl font-extrabold mb-4 bg-gradient-to-r from-purple-400 to-blue-400 text-transparent bg-clip-text drop-shadow-[0_0_25px_rgba(139,92,246,0.5)] tracking-tight">
            BioInfo Nexus
          </h1>
          <p className="text-slate-400 text-lg md:text-xl font-light">
            Federated Search Engine for RCSB PDB & NCBI
          </p>
        </header>

        <form onSubmit={handleSearch} className="w-full max-w-2xl relative mb-12">
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl blur-md opacity-25 group-hover:opacity-40 transition duration-500"></div>
            <div className="relative flex items-center bg-slate-800/80 backdrop-blur-xl border border-slate-700 rounded-2xl p-2 shadow-2xl transition-all focus-within:border-purple-500 focus-within:ring-1 focus-within:ring-purple-500">
              <input
                type="text"
                className="w-full bg-transparent text-white placeholder-slate-400 px-4 py-3 outline-none text-lg"
                placeholder="Enter Gene or PDB ID (e.g., BRCA1, 4HHB)..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="bg-purple-600 hover:bg-purple-500 text-white p-3 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[56px]"
              >
                {loading ? <Loader2 className="animate-spin w-6 h-6" /> : <Search className="w-6 h-6" />}
              </button>
            </div>
          </div>
        </form>

        {error && (
          <div className="w-full max-w-2xl glass-card p-6 border-red-500/30 flex items-start gap-4 text-red-200 mb-8">
            <AlertCircle className="w-6 h-6 text-red-400 shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-red-400 text-lg mb-1">Search Error</h3>
              <p className="text-sm">{error}</p>
            </div>
          </div>
        )}

        {result && !loading && (
          <div className="w-full max-w-6xl grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* PDB Card */}
            <div className={`glass-card flex flex-col h-full transform hover:-translate-y-1 transition-all duration-300 ${result.pdb_result.status === 'error' ? 'border-yellow-500/50 bg-yellow-500/5' : ''}`}>
              <div className="p-6 border-b border-white/10 flex flex-col h-[140px]">
                <div className="inline-flex items-center gap-2 bg-blue-500/20 text-blue-300 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider w-max mb-4">
                  <Database className="w-3 h-3" /> RCSB PDB
                </div>
                <h2 className="text-xl font-bold text-white line-clamp-2 leading-tight">
                  {result.pdb_result.status === 'success' ? (result.pdb_result.data?.title || 'Structure Unknown') : 'Structure Unknown'}
                </h2>
              </div>
              <div className="p-6 flex-grow flex flex-col gap-4">
                {result.pdb_result.status === 'success' && result.pdb_result.data ? (
                  <>
                    <div className="flex flex-col pb-3 border-b border-white/5">
                      <span className="text-xs text-slate-400 uppercase tracking-wider mb-1">PDB ID</span>
                      <strong className="text-white font-mono text-lg">{result.pdb_result.data.entry_id}</strong>
                    </div>
                    <div className="flex flex-col pb-3 border-b border-white/5">
                      <span className="text-xs text-slate-400 uppercase tracking-wider mb-1">Method</span>
                      <strong className="text-slate-200">
                        {result.pdb_result.data.experimental_method?.join(', ') || 'N/A'}
                      </strong>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-xs text-slate-400 uppercase tracking-wider mb-1">Resolution</span>
                      <strong className="text-slate-200">
                        {result.pdb_result.data.resolution_combined?.map(r => `${r}Å`).join(', ') || 'N/A'}
                      </strong>
                    </div>
                  </>
                ) : result.pdb_result.status === 'error' ? (
                  <div className="flex-grow flex flex-col items-center justify-center text-yellow-400/80 py-8 text-center">
                    <AlertCircle className="w-12 h-12 mb-4 opacity-50" />
                    <p className="font-semibold mb-2">Sync Failed</p>
                    <p className="text-sm opacity-80">{result.pdb_result.error_message}</p>
                  </div>
                ) : (
                  <div className="flex-grow flex flex-col items-center justify-center text-slate-400 py-8 text-center">
                    <Database className="w-12 h-12 mb-4 opacity-20" />
                    <p>No structural data found</p>
                  </div>
                )}
              </div>
            </div>

            {/* NCBI Card */}
            <div className={`glass-card flex flex-col h-full transform hover:-translate-y-1 transition-all duration-300 ${result.ncbi_result.status === 'error' ? 'border-yellow-500/50 bg-yellow-500/5' : ''}`}>
              <div className="p-6 border-b border-white/10 flex flex-col h-[140px]">
                <div className="inline-flex items-center gap-2 bg-purple-500/20 text-purple-300 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider w-max mb-4">
                  <Dna className="w-3 h-3" /> NCBI Gene
                </div>
                <h2 className="text-xl font-bold text-white line-clamp-2 leading-tight">
                  {result.ncbi_result.status === 'success' ? (result.ncbi_result.data?.description || 'Gene Unknown') : 'Gene Unknown'}
                </h2>
              </div>
              <div className="p-6 flex-grow flex flex-col gap-4">
                {result.ncbi_result.status === 'success' && result.ncbi_result.data ? (
                  <>
                    <div className="flex flex-col pb-3 border-b border-white/5">
                      <span className="text-xs text-slate-400 uppercase tracking-wider mb-1">Gene ID</span>
                      <strong className="text-white font-mono text-lg">{result.ncbi_result.data.gene_id}</strong>
                    </div>
                    <div className="flex flex-col pb-3 border-b border-white/5">
                      <span className="text-xs text-slate-400 uppercase tracking-wider mb-1">Symbol</span>
                      <strong className="text-slate-200">{result.ncbi_result.data.name || 'N/A'}</strong>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-xs text-slate-400 uppercase tracking-wider mb-1">Organism</span>
                      <strong className="text-slate-200">{result.ncbi_result.data.organism || 'N/A'}</strong>
                    </div>
                  </>
                ) : result.ncbi_result.status === 'error' ? (
                  <div className="flex-grow flex flex-col items-center justify-center text-yellow-400/80 py-8 text-center">
                    <AlertCircle className="w-12 h-12 mb-4 opacity-50" />
                    <p className="font-semibold mb-2">Sync Failed</p>
                    <p className="text-sm opacity-80">{result.ncbi_result.error_message}</p>
                  </div>
                ) : (
                  <div className="flex-grow flex flex-col items-center justify-center text-slate-400 py-8 text-center">
                    <Dna className="w-12 h-12 mb-4 opacity-20" />
                    <p>No gene summary found</p>
                  </div>
                )}
              </div>
            </div>

            {/* UniProt Card */}
            <div className={`glass-card flex flex-col h-full transform hover:-translate-y-1 transition-all duration-300 ${result.uniprot_result.status === 'error' ? 'border-yellow-500/50 bg-yellow-500/5' : ''}`}>
              <div className="p-6 border-b border-white/10 flex flex-col h-[140px]">
                <div className="inline-flex items-center gap-2 bg-emerald-500/20 text-emerald-300 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider w-max mb-4">
                  <Database className="w-3 h-3" /> UniProtKB
                </div>
                <h2 className="text-xl font-bold text-white line-clamp-2 leading-tight">
                  {result.uniprot_result.status === 'success' ? (result.uniprot_result.data?.protein_name || 'Protein Unknown') : 'Protein Unknown'}
                </h2>
              </div>
              <div className="p-6 flex-grow flex flex-col gap-4">
                {result.uniprot_result.status === 'success' && result.uniprot_result.data ? (
                  <>
                    <div className="flex flex-col pb-3 border-b border-white/5">
                      <span className="text-xs text-slate-400 uppercase tracking-wider mb-1">Accession</span>
                      <strong className="text-white font-mono text-lg">{result.uniprot_result.data.primary_accession}</strong>
                    </div>
                    <div className="flex flex-col pb-3 border-b border-white/5">
                      <span className="text-xs text-slate-400 uppercase tracking-wider mb-1">Organism</span>
                      <strong className="text-slate-200">{result.uniprot_result.data.organism || 'N/A'}</strong>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-xs text-slate-400 uppercase tracking-wider mb-1">Sequence Length</span>
                      <strong className="text-slate-200">
                        {result.uniprot_result.data.sequence_length ? `${result.uniprot_result.data.sequence_length} aa` : 'N/A'}
                      </strong>
                    </div>
                  </>
                ) : result.uniprot_result.status === 'error' ? (
                  <div className="flex-grow flex flex-col items-center justify-center text-yellow-400/80 py-8 text-center">
                    <AlertCircle className="w-12 h-12 mb-4 opacity-50" />
                    <p className="font-semibold mb-2">Sync Failed</p>
                    <p className="text-sm opacity-80">{result.uniprot_result.error_message}</p>
                  </div>
                ) : (
                  <div className="flex-grow flex flex-col items-center justify-center text-slate-400 py-8 text-center">
                    <Database className="w-12 h-12 mb-4 opacity-20" />
                    <p>No protein data found</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
