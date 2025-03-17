# Estrattore Dati ISTAT

Piccolo tool per scaricare dati dai dataflow ISTAT.

Per utilizzarlo basta inserire l'identificativo del dataflow richiesto (es: 122_54) e se i dati risultanti debbano essere in italiano o in inglese(it, en).

In particolare estrarrà:

- Le sottocategorie dei dataflow(esç 122_54_DCSC_TUR_1)
- La datastructure che definisice la struttura del dataflow
- Le codelist con i codici associati

## 🔽 Installazione

**Scarica o clona** la libreria dal repository.
**Estrai l'archivio** in una cartella a tua scelta.

## 🚀 Esecuzione

**Clicca** su `run.bat` per avviare il processo.

## 📂 Risultati

I dati estratti saranno disponibili nella cartella **`extracted/`**, suddivisi in:

- 📄 **CSV** (per le dimensioni tabellari)
- 📝 **JSON** (per i dati strutturati)

📢 _Assicurati di avere Python installato sul tuo sistema prima di eseguire il file BAT._
