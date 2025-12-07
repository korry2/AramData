import requests
import json

# --- ARAM KRALLARI (MANUEL LİSTE) ---
# İstatistiksel olarak ARAM'da kazanma oranı hep yüksek olanlar
ARAM_GODS = [
    "AurelionSol", "Veigar", "Pyke", "Katarina", "Samira", "MasterYi", 
    "Brand", "Morgana", "Lux", "Jhin", "MissFortune", "Senna", 
    "Blitzcrank", "Nautilus", "Malphite", "Sona", "Seraphine", "Swain"
]

# --- ARAM ZAYIFLARI ---
# Genelde ARAM'da zorlananlar
ARAM_WEAK = [
    "Evelynn", "Bard", "RekSai", "Ivern", "Elise"
]

def get_latest_version():
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    try:
        response = requests.get(url)
        return response.json()[0]
    except:
        return "14.23.1"

def generate_aram_tierlist():
    version = get_latest_version()
    print(f"Versiyon: {version}")
    
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/tr_TR/champion.json"
    data = requests.get(url).json()["data"]
    
    tier_list = {
        "S+": [], # Kazanma Garantili
        "S": [],  # Çok Güçlü
        "A": [],  # İyi
        "B": []   # Ortalama/Zayıf
    }
    
    for name, info in data.items():
        tags = info["tags"]
        stats = info["stats"]
        
        # 1. Önce Manuel Listeye Bak
        if name in ARAM_GODS:
            tier_list["S+"].append(name)
            continue
        if name in ARAM_WEAK:
            tier_list["B"].append(name)
            continue
            
        # 2. Algoritmik Dağıtım
        # Menzilli ve Büyücüler/Nişancılar genelde iyidir
        if "Mage" in tags or "Marksman" in tags:
            tier_list["S"].append(name)
        
        # Tanklar ve Destekler her zaman iş yapar
        elif "Tank" in tags or "Support" in tags:
            tier_list["A"].append(name)
            
        # Suikastçılar ve Dövüşçüler takım kompozisyonuna bakar
        else:
            tier_list["A"].append(name)
            
    # Listeyi kaydet
    with open("tierlist.json", "w", encoding="utf-8") as f:
        json.dump(tier_list, f, indent=4, ensure_ascii=False)
    
    print("ARAM Tier Listesi (Hibrit Zeka) başarıyla güncellendi!")

if __name__ == "__main__":
    generate_aram_tierlist()
