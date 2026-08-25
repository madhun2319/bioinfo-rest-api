document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('searchBtn');
    const searchInput = document.getElementById('searchInput');
    const loader = document.getElementById('loader');
    
    // Cards
    const pdbCard = document.getElementById('pdbCard');
    const ncbiCard = document.getElementById('ncbiCard');
    const errorState = document.getElementById('errorState');
    
    // PDB Elements
    const pdbTitle = document.getElementById('pdbTitle');
    const pdbId = document.getElementById('pdbId');
    const pdbOrganism = document.getElementById('pdbOrganism');
    const pdbMethod = document.getElementById('pdbMethod');
    const pdbResolution = document.getElementById('pdbResolution');
    
    // NCBI Elements
    const ncbiTitle = document.getElementById('ncbiTitle');
    const ncbiId = document.getElementById('ncbiId');
    const ncbiSymbol = document.getElementById('ncbiSymbol');
    const ncbiOrganism = document.getElementById('ncbiOrganism');
    const ncbiDesc = document.getElementById('ncbiDesc');

    const handleSearch = async () => {
        const query = searchInput.value.trim();
        if (!query) return;

        // Reset UI
        pdbCard.classList.remove('visible');
        pdbCard.classList.add('hidden');
        ncbiCard.classList.remove('visible');
        ncbiCard.classList.add('hidden');
        errorState.classList.add('hidden');
        
        loader.style.display = 'block';

        try {
            const response = await fetch(`/api/aggregate?term=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            loader.style.display = 'none';

            let foundAny = false;

            if (data.pdb_result) {
                foundAny = true;
                pdbTitle.textContent = data.pdb_result.title || "Unknown Structure";
                pdbId.textContent = data.pdb_result.pdb_id.toUpperCase();
                pdbOrganism.textContent = data.pdb_result.organism || "N/A";
                pdbMethod.textContent = data.pdb_result.experimental_method || "N/A";
                pdbResolution.textContent = data.pdb_result.resolution ? `${data.pdb_result.resolution} Å` : "N/A";
                
                pdbCard.classList.remove('hidden');
                setTimeout(() => pdbCard.classList.add('visible'), 50);
            }

            if (data.ncbi_result) {
                foundAny = true;
                ncbiTitle.textContent = data.ncbi_result.name || "Unknown Gene";
                ncbiId.textContent = data.ncbi_result.gene_id;
                ncbiSymbol.textContent = data.ncbi_result.name || "N/A";
                ncbiOrganism.textContent = data.ncbi_result.organism || "N/A";
                ncbiDesc.textContent = data.ncbi_result.description || "No description available.";
                
                ncbiCard.classList.remove('hidden');
                setTimeout(() => ncbiCard.classList.add('visible'), 150);
            }

            if (!foundAny) {
                errorState.classList.remove('hidden');
                errorState.classList.add('visible');
            }

        } catch (err) {
            loader.style.display = 'none';
            errorState.classList.remove('hidden');
            errorState.classList.add('visible');
            errorState.querySelector('h3').textContent = "Network Error";
            errorState.querySelector('p').textContent = "Failed to connect to the BioInfo API.";
        }
    };

    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSearch();
    });
});
