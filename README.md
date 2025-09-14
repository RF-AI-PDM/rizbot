# rizbot
membangun chatbot Predictive Maintenance (PdM) yang mampu:
## 📊 Flowchart Alur Chatbot Predictive Maintenance

```text
+------------------+
|   User Input     |
| (Pertanyaan PdM) |
+--------+---------+
         |
         v
+----------------------+
|   Intent Detection   |
| (sapaan, analisis,   |
| rekomendasi, dll.)   |
+----------+-----------+
           |
   +-------+--------+
   |                |
   v                v
+-----------+   +----------------+
| Data Ada? |   | Data Tidak Ada |
+-----+-----+   +----------------+
      | Yes               |
      v                   v
+----------------+   +----------------------------+
| Analisis Data  |   | "Data tidak tersedia,      |
| (Vibrasi, DGA, |   | silakan upload file baru." |
|  MCSA, Oil)    |   +----------------------------+
+-------+--------+
        |
        v
+----------------------+
| Generate Rekomendasi |
| (Maintenance Action) |
+---------+------------+
          |
          v
+----------------------+
|   Chatbot Response   |
| (Jawaban ke user)    |
+----------------------+
