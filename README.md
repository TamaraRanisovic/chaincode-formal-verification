# chaincode-formal-verification

Ovaj repozitorijum sadrži implementaciju pametnog ugovora za upravljanje podacima o proizvodima i njihovim ocenama, zajedno sa pomoćnim alatima za testiranje i verifikaciju.

# Struktura repozitorijuma

first_sc – sadrži pametan ugovor namenjen za upravljanje podacima o proizvodima i njihovim ocenama, napisan u programskom jeziku Go za Hyperledger Fabric (HLF) platformu, zajedno sa detaljnim uputstvom za njegovo pokretanje i testiranje

rest-api-go – jednostavna Go aplikacija koja funkcioniše kao server za obradu REST zahteva i omogućava interakciju sa pametnim ugovorom. Aplikacija je preuzeta iz fabric-samples repozitorijuma (modul asset-transfer-basic) i prilagođena za potrebe ovog projekta.

Z3.ipynb - formalna verifikacija pojednostavljenog modela proizvoda i ocena korišćenjem Z3 solvera

coq_verification.v - formalna verifikacija pojednostavljenog modela proizvoda i ocena korišćenjem Rocq/Coq interaktivnog dokazivača teorema

monte_carlo_test.ipynb - Monte Carlo testiranje pojednostavljenog modela proizvoda i ocena kroz veliki broj nasumičnih operacija radi empirijske provere očuvanja definisanih invarijanti sistema

performance_test - benchmark testovi osnovnih funkcionalnosti sistema, koji mere vreme izvršavanja invoke i query operacija (pojedinačnih i batch) nad proizvodima, radi procene performansi i skalabilnosti sistema.

Napomena: Pre testiranja pametnog ugovora, neophodno je pratiti uputstvo za instalaciju potrebnog softvera i preuzimanje fabric-samples repozitorijuma sa zvaničnog HLF sajta:

https://hyperledger-fabric.readthedocs.io/en/release-2.4/getting_started.html

Nakon toga, sledite uputstvo za pokretanje koje se nalazi unutar first_sc direktorijuma.
