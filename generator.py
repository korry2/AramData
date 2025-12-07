import requests
import json
import os

def get_latest_version():
    """En güncel LoL sürümünü bulur."""
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    try:
        response = requests.get(url)
        return response.json()[0]
    except:
        return "14.23.1"

def generate_aram_tierlist():
    """Şampiyonları çeker ve ARAM mantığına göre sınıflandırır."""
    version = get_latest_version()
    print(f"Versiyon: {version}")
    
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/tr_TR/champion.json"
    data = requests.get(url).json()["data"]
    
    # ARAM Tier List Mantığı (Simülasyon)
    # Gerçek hayatta buraya u.gg gibi sitelerden veri çeken kodlar eklenir.
    # Şimdilik "Menzilli ve Alan Etkili" şampiyonları S Tier yapıyoruz.
    
    tier_list = {
        "S+": [],
        "S": [],
        "A": [],
        "B": []
    }
    
    # Basit bir algoritma ile listeyi dolduralım
    for name, info in data.items():
        tags = info["tags"]
        stats = info["stats"]
        
        # S+ KRİTERLERİ: Büyücü (Mage) veya Nişancı (Marksman)
        if "Mage" in tags or "Marksman" in tags:
            # Biraz seçici olalım, canı az ama hasarı çok olanlar (Poke)
            if stats["hpperlevel"] < 95: 
                tier_list["S+"].append(name)
            else:
                tier_list["S"].append(name)
        
        # S KRİTERLERİ: Destek (Support) veya Tank (Canı yüksek)
        elif "Support" in tags or "Tank" in tags:
            tier_list["S"].append(name)
            
        # Diğerleri A ve B
        elif "Assassin" in tags:
            tier_list["A"].append(name)
        else:
            tier_list["B"].append(name)
            
    # Sonucu kaydet
    with open("tierlist.json", "w", encoding="utf-8") as f:
        json.dump(tier_list, f, indent=4, ensure_ascii=False)
    
    print("Tier list başarıyla oluşturuldu!")

if __name__ == "__main__":
    generate_aram_tierlist()
