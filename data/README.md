# Dataset Information

## IEEE-dga.csv

Dataset ini berisi data DGA (Dissolved Gas Analysis) berdasarkan IEEE Std C57.104™-2019.

### Deskripsi
- **Source**: IEEE Guide for the Interpretation of Gases Generated in Mineral Oil-Immersed Transformers
- **Standard**: IEEE Std C57.104™-2019 (Revision of IEEE Std C57.104-2008)
- **Format**: CSV (Comma Separated Values)

### Kegunaan
Dataset ini digunakan untuk:
1. Training machine learning models untuk klasifikasi gangguan trafo
2. Referensi interpretasi hasil DGA
3. Benchmarking metode diagnosis
4. Penelitian dan pengembangan sistem PdM

### Gas Parameters
Dataset mencakup gas-gas berikut:
- **H2** - Hydrogen
- **CH4** - Methane
- **C2H2** - Acetylene
- **C2H4** - Ethylene
- **C2H6** - Ethane
- **CO** - Carbon Monoxide
- **CO2** - Carbon Dioxide

### Fault Types
Jenis gangguan yang dapat diidentifikasi:
1. **PD** - Partial Discharge
2. **D1** - Discharge of low energy
3. **D2** - Discharge of high energy
4. **T1** - Thermal fault < 300°C
5. **T2** - Thermal fault 300-700°C
6. **T3** - Thermal fault > 700°C

### Citation
Jika menggunakan dataset ini dalam publikasi, mohon sitasi:
```
IEEE Std C57.104™-2019, "IEEE Guide for the Interpretation of Gases 
Generated in Mineral Oil-Immersed Transformers," IEEE Power and Energy Society, 2019.
```

### License
Dataset ini digunakan untuk tujuan pendidikan dan penelitian sesuai dengan IEEE standards licensing.
