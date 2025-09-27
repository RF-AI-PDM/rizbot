"""
Data Generator untuk menambah variasi training data
Menghasilkan synthetic data untuk meningkatkan performa model
"""

import json
import random
from typing import List, Dict

class PdMDataGenerator:
    """
    Generator untuk membuat additional training data untuk PdM chatbot
    """
    
    def __init__(self):
        self.vibration_terms = [
            "vibration", "getaran", "oscillation", "vibrasi", "shake", "goyangan",
            "acceleration", "percepatan", "frequency", "frekuensi", "amplitude", "amplitudo",
            "bearing", "bantalan", "misalignment", "unbalance", "looseness"
        ]
        
        self.mcsa_terms = [
            "current", "arus", "motor", "electrical", "listrik", "rotor", "stator",
            "broken bar", "eccentricity", "load", "beban", "power", "daya",
            "harmonics", "harmonik", "sideband", "spektrum"
        ]
        
        self.dga_terms = [
            "gas", "dissolved", "terlarut", "transformer", "trafo", "oil", "minyak",
            "hydrogen", "hidrogen", "methane", "metana", "acetylene", "asetilen",
            "ethylene", "etilen", "carbon monoxide", "karbon monoksida"
        ]
        
        self.maintenance_terms = [
            "maintenance", "perawatan", "service", "repair", "perbaikan", "schedule",
            "jadwal", "preventive", "predictive", "corrective", "emergency",
            "reliability", "keandalan", "failure", "kegagalan"
        ]
    
    def generate_patterns(self, base_patterns: List[str], terms: List[str], count: int = 5) -> List[str]:
        """
        Generate variasi patterns dengan menambahkan terms yang relevan
        """
        generated = []
        templates = [
            "bagaimana cara {}",
            "jelaskan tentang {}",
            "apa itu {}",
            "cara analisis {}",
            "prosedur {}",
            "metode {}",
            "teknik {}",
            "panduan {}",
            "tutorial {}",
            "contoh {}"
        ]
        
        for _ in range(count):
            template = random.choice(templates)
            term = random.choice(terms)
            generated.append(template.format(term))
        
        return generated + base_patterns
    
    def enhance_intents(self, intents_file: str = "data/intents.json", output_file: str = "data/enhanced_intents.json"):
        """
        Enhance existing intents dengan patterns tambahan
        """
        # Load existing intents
        with open(intents_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Enhance each intent
        for intent in data['intents']:
            tag = intent['tag']
            
            if 'vibration' in tag or any(term in tag for term in ['vibration', 'getaran']):
                intent['patterns'] = self.generate_patterns(
                    intent['patterns'], self.vibration_terms, 8
                )
            
            elif 'mcsa' in tag or 'current' in tag:
                intent['patterns'] = self.generate_patterns(
                    intent['patterns'], self.mcsa_terms, 6
                )
            
            elif 'dga' in tag or 'gas' in tag:
                intent['patterns'] = self.generate_patterns(
                    intent['patterns'], self.dga_terms, 6
                )
            
            elif 'maintenance' in tag:
                intent['patterns'] = self.generate_patterns(
                    intent['patterns'], self.maintenance_terms, 10
                )
        
        # Add new intents untuk diagnostic scenarios
        additional_intents = [
            {
                "tag": "bearing_diagnosis",
                "patterns": [
                    "bearing rusak",
                    "bantalan bermasalah", 
                    "bearing noise",
                    "suara bearing aneh",
                    "inner race defect",
                    "outer race defect",
                    "ball defect",
                    "cage defect",
                    "bearing frequency",
                    "BPFI BPFO"
                ],
                "responses": [
                    "Untuk diagnosis bearing, perhatikan frekuensi karakteristik: BPFI (inner race), BPFO (outer race), BSF (ball spin), FTF (cage). Amplitudo tinggi pada frekuensi ini menunjukkan defect.",
                    "Bearing rusak ditandai dengan peningkatan amplitudo pada bearing frequencies. Gunakan envelope analysis untuk deteksi dini.",
                    "Analisis spektrum vibrasi pada range 1-10 kHz. Peak pada bearing characteristic frequencies mengindikasikan kerusakan spesifik."
                ]
            },
            {
                "tag": "unbalance_diagnosis", 
                "patterns": [
                    "unbalance",
                    "ketidakseimbangan",
                    "rotor unbalance",
                    "static unbalance",
                    "dynamic unbalance",
                    "balancing",
                    "penyeimbangan"
                ],
                "responses": [
                    "Unbalance terdeteksi dari peak tinggi pada 1x RPM (running speed). Static unbalance: peak radial sama semua arah. Dynamic unbalance: peak axial berbeda.",
                    "Untuk koreksi unbalance, gunakan metode trial weight. Tambahkan massa trial, ukur perubahan amplitudo dan phase.",
                    "Unbalance severity berdasarkan ISO 21940: Grade G2.5 untuk motor presisi, G6.3 untuk motor industri standar."
                ]
            },
            {
                "tag": "motor_fault_diagnosis",
                "patterns": [
                    "motor fault",
                    "kerusakan motor",
                    "motor problem",
                    "motor diagnostic",
                    "electric motor analysis",
                    "induction motor fault"
                ],
                "responses": [
                    "Fault motor meliputi: electrical (broken rotor bar, stator winding), mechanical (bearing, unbalance), dan magnetic (eccentricity). Gunakan kombinasi MCSA dan vibration analysis.",
                    "Broken rotor bar: sideband di (1±2s)f dimana s=slip. Stator fault: harmonik ganjil. Eccentricity: sideband di f±fr.",
                    "Motor diagnostic matrix: vibration untuk mechanical fault, current signature untuk electrical fault, thermal untuk insulation degradation."
                ]
            }
        ]
        
        data['intents'].extend(additional_intents)
        
        # Save enhanced intents
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Enhanced intents disimpan ke {output_file}")
        return data

def main():
    """
    Generate enhanced training data
    """
    generator = PdMDataGenerator()
    generator.enhance_intents()

if __name__ == "__main__":
    main()