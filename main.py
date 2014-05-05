import os
import jinja2
import webapp2
import models
import logging
from google.appengine.ext import db
from google.appengine.api import users


template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

spdetail_properties=["Taxcd", "Syncd", "family_code", "genus", "species", "authority", "subsp", "variety", "forma", "subsp_auth", "var_auth", "forma_auth", "sub_family", "tribe", "common", "Wisc_found", "ssp", "var", "f", "hybrids", "status_code", "hide", "USDA", "COFC", "WETINDICAT", "FAM_NAME", "FAMILY", "GC", "FAMILY_COMMON", "SYNWisc_found", "SYNS_STATUS", "SYNV_STATUS", "SYNF_STATUS", "SYNHYBRIDS_STATUS", "SYNW_STATUS", "speciesweb_Taxcd", "Status", "Photo", "Photographer", "Thumbmaps", "Accgenus", "SORTOR", "Hand", "growth_habit_bck", "blooming_dt_bck", "origin_bck", "Thumbphoto", "date_time", "growth_habit", "blooming_dt", "origin", "Taxa"]

#familyList was obtained like this:
# select DISTINCT Family from spdetail WHERE Syncd = '.' AND Wisc_Found = 'W' INTO OUTFILE "/tmp/family"
# cat /tmp/family4 | sort |tr '\n' ' '|sed 's/ /","/g'
#familyList = ["Acanthaceae","Aceraceae","Acoraceae","Actinidiaceae","Adoxaceae","Agavaceae","Aizoaceae","Alismataceae","Amaranthaceae","Anacardiaceae","Annonaceae","Apiaceae","Apocynaceae","Aquifoliaceae","Araceae","Araliaceae","Araucariaceae","Arecaceae","Aristolochiaceae","Asclepiadaceae","Aspleniaceae","Asteraceae","Azollaceae","Balanopaceae","Balsaminaceae","Bataceae","Begoniaceae","Berberidaceae","Betulaceae","Bignoniaceae","Blechnaceae","Bombacaceae","Boraginaceae","Brassicaceae","Bromeliaceae","Brunelliaceae","Buddlejaceae","Burseraceae","Butomaceae","Buxaceae","Cabombaceae","Cactaceae","Caesalpiniaceae","Callitrichaceae","Calycanthaceae","Campanulaceae","Cannabaceae","Capparidaceae","Caprifoliaceae","Caryocaraceae","Caryophyllaceae","Cecropiaceae","Celastraceae","Ceratophyllaceae","Chenopodiaceae","Chloranthaceae","Chrysobalanaceae","Cistaceae","Clethraceae","Clusiaceae","Combretaceae","Commelinaceae","Connaraceae","Convolvulaceae","Cornaceae","Costaceae","Crassulaceae","Crossosomataceae","Cucurbitaceae","Cupressaceae","Cuscutaceae","Cyatheaceae","Cyperaceae","Cyrillaceae","Datiscaceae","Dennstaedtiaceae","Dichapetalaceae","Dilleniaceae","Dioscoreaceae","Dipsacaceae","Dipterocarpaceae","Droseraceae","Dryopteridaceae","Ebenaceae","Elaeagnaceae","Elaeocarpaceae","Elatinaceae","Empetraceae","Ephedraceae","Equisetaceae","Eremolepidaceae","Ericaceae","Eriocaulaceae","Erythroxylaceae","Euphorbiaceae","Fabaceae","Fagaceae","Flacourtiaceae","Fouquieriaceae","Frankeniaceae","Fumariaceae","Garryaceae","Gentianaceae","Geraniaceae","Gesneriaceae","Ginkgoaceae","Goodeniaceae","Grossulariaceae","Haemodoraceae","Haloragaceae","Hamamelidaceae","Heliconiaceae","Hernandiaceae","Hippocastanaceae","Hippocrateaceae","Hippuridaceae","Humiriaceae","Hydrangeaceae","Hydrocharitaceae","Hydrophyllaceae","Hypericaceae","Icacinaceae","Iridaceae","Isoetaceae","Ixonanthaceae","Juglandaceae","Juncaceae","Juncaginaceae","Krameriaceae","Lacistemataceae","Lamiaceae","Lardizabalaceae","Lauraceae","Lecythidaceae","Leeaceae","Lemnaceae","Lentibulariaceae","Liliaceae","Limnanthaceae","Limnocharitaceae","Linaceae","Loasaceae","Lobeliaceae","Loganiaceae","Loranthaceae","Lycopodiaceae","Lythraceae","Magnoliaceae","Malpighiaceae","Malvaceae","Marantaceae","Marcgraviaceae","Marsileaceae","Melastomataceae","Meliaceae","Mendonciaceae","Menispermaceae","Menyanthaceae","Mimosaceae","Molluginaceae","Monimiaceae","Monotropaceae","Moraceae","Myricaceae","Myristicaceae","Myrsinaceae","Myrtaceae","Najadaceae","Nelumbonaceae","Nyctaginaceae","Nymphaeaceae","Nyssaceae","Ochnaceae","Olacaceae","Oleaceae","Onagraceae","Ophioglossaceae","Opiliaceae","Orchidaceae","Orobanchaceae","Osmundaceae","Oxalidaceae","Paeoniaceae","Pandanaceae","Papaveraceae","Passifloraceae","Pedaliaceae","Phytolaccaceae","Pinaceae","Piperaceae","Plantaginaceae","Platanaceae","Plumbaginaceae","Poaceae","Podocarpaceae","Podostemaceae","Polemoniaceae","Polygalaceae","Polygonaceae","Polypodiaceae","Pontederiaceae","Portulacaceae","Potamogetonaceae","Primulaceae","Proteaceae","Pteridaceae","Pyrolaceae","Quiinaceae","Ranunculaceae","Rapateaceae","Resedaceae","Restionaceae","Rhamnaceae","Rhizophoraceae","Rosaceae","Rubiaceae","Ruppiaceae","Rutaceae","Sabiaceae","Salicaceae","Santalaceae","Sapindaceae","Sapotaceae","Sarraceniaceae","Saururaceae","Saxifragaceae","Scheuchzeriaceae","Scrophulariaceae","Selaginellaceae","Simaroubaceae","Smilacaceae","Solanaceae","Sonneratiaceae","Sparganiaceae","Sphaerosepalaceae","Staphyleaceae","Sterculiaceae","Symplocaceae","Tamaricaceae","Taxaceae","Taxodiaceae","Theaceae","Thelypteridaceae","Theophrastaceae","Thymelaeaceae","Tiliaceae","Trapaceae","Typhaceae","Ulmaceae","Urticaceae","Valerianaceae","Verbenaceae","Violaceae","Viscaceae","Vitaceae","Vittariaceae","Vochysiaceae","Xyridaceae","Zannichelliaceae","Zygophyllaceae"]

familyList = ["Acanthaceae","Aceraceae","Acoraceae","Adoxaceae","Agavaceae","Aizoaceae","Alismataceae","Amaranthaceae","Anacardiaceae","Annonaceae","Apiaceae","Apocynaceae","Aquifoliaceae","Araceae","Araliaceae","Aristolochiaceae","Asclepiadaceae","Aspleniaceae","Asteraceae","Azollaceae","Balsaminaceae","Berberidaceae","Betulaceae","Bignoniaceae","Boraginaceae","Brassicaceae","Butomaceae","Buxaceae","Cabombaceae","Cactaceae","Caesalpiniaceae","Callitrichaceae","Campanulaceae","Cannabaceae","Capparidaceae","Caprifoliaceae","Caryophyllaceae","Celastraceae","Ceratophyllaceae","Chenopodiaceae","Cistaceae","Commelinaceae","Convolvulaceae","Cornaceae","Crassulaceae","Cucurbitaceae","Cupressaceae","Cuscutaceae","Cyperaceae","Dennstaedtiaceae","Dioscoreaceae","Dipsacaceae","Droseraceae","Dryopteridaceae","Elaeagnaceae","Elatinaceae","Equisetaceae","Ericaceae","Eriocaulaceae","Euphorbiaceae","Fabaceae","Fagaceae","Fumariaceae","Gentianaceae","Geraniaceae","Grossulariaceae","Haloragaceae","Hamamelidaceae","Hippocastanaceae","Hippuridaceae","Hydrangeaceae","Hydrocharitaceae","Hydrophyllaceae","Hypericaceae","Iridaceae","Isoetaceae","Juglandaceae","Juncaceae","Juncaginaceae","Lamiaceae","Lauraceae","Lemnaceae","Lentibulariaceae","Liliaceae","Limnanthaceae","Linaceae","Lobeliaceae","Lycopodiaceae","Lythraceae","Malvaceae","Melastomataceae","Menispermaceae","Menyanthaceae","Mimosaceae","Molluginaceae","Monotropaceae","Moraceae","Myricaceae","Najadaceae","Nelumbonaceae","Nyctaginaceae","Nymphaeaceae","Nyssaceae","Oleaceae","Onagraceae","Ophioglossaceae","Orchidaceae","Orobanchaceae","Osmundaceae","Oxalidaceae","Papaveraceae","Pedaliaceae","Phytolaccaceae","Pinaceae","Plantaginaceae","Platanaceae","Poaceae","Polemoniaceae","Polygalaceae","Polygonaceae","Polypodiaceae","Pontederiaceae","Portulacaceae","Potamogetonaceae","Primulaceae","Pteridaceae","Pyrolaceae","Ranunculaceae","Resedaceae","Rhamnaceae","Rosaceae","Rubiaceae","Ruppiaceae","Rutaceae","Salicaceae","Santalaceae","Sarraceniaceae","Saururaceae","Saxifragaceae","Scheuchzeriaceae","Scrophulariaceae","Selaginellaceae","Simaroubaceae","Smilacaceae","Solanaceae","Sparganiaceae","Staphyleaceae","Taxaceae","Thelypteridaceae","Thymelaeaceae","Tiliaceae","Typhaceae","Ulmaceae","Urticaceae","Valerianaceae","Verbenaceae","Violaceae","Viscaceae","Vitaceae","Xyridaceae","Zannichelliaceae","Zygophyllaceae"]

#genusList = ["Abarema","Abies","Abortopetalum","Abronia","Abuta","Abutilon","Acacia","Acalypha","Acanthopanax","Acanthosyris","Acer","Acerates","Acetosa","Acetosella","Achillea","Achimenes","Achnatherum","Achroanthes","Achyranthes","Acicalyptus","Acinos","Acmella","Acmispon","Acnida","Acnistus","Aconitum","Acorus","Acosta","Acourtia","Acroptilon","Acrostichum","Actaea","Actinomeris","Acuan","Adansonia","Addisonia","Adenanthe","Adenanthos","Adenocaulon","Adiantum","Adicea","Adinandra","Adlumia","Adopogon","Adoxa","Aegilops","Aegiphila","Aegopodium","Aesculus","Aetanthus","Aethionema","Aethusa","Afrormosia","Afzelia","Agalinis","Agaloma","Agarista","Agastache","Agave","Ageratina","Ageratum","Aglaia","Agonandra","Agonis","Agoseris","Agrimonia","Agropyron","Agrostemma","Agrostis","Ailanthus","Aiouea","Aira","Ajuga","Akebia","Albizia","Albizzia","Alcea","Alchemilla","Alchornea","Alectryon","Aletris","Alguelagum","Alisma","Allenrolfea","Alliaria","Allionia","Allium","Allocarya","Alloneuron","Allophylus","Alloplectus","Alnus","Alonsoa","Alopecurus","Alophia","Aloysia","Alsinanthe","Alsine","Alsodeia","Althaea","Alyssum","Alyxia","Amaioua","Amaranthus","Amarella","Ambrina","Ambrosia","Amelanchier","Amellus","Amerorchis","Amesia","Ammannia","Ammophila","Amorpha","Ampelamus","Ampelopsis","Amphiachyris","Amphicarpaea","Amsinckia","Amsonia","Amygdalus","Anacardium","Anacharis","Anagallis","Anaphalis","Anaxagorea","Anchusa","Andira","Andrachne","Androcalymma","Androcera","Andromeda","Andropogon","Androsace","Anemarrhena","Anemone","Anemonella","Anemopaegma","Anethum","Angelica","Aniba","Anisomeris","Anneslia","Anoda","Anogra","Anomospermum","Anoplanthus","Antennaria","Antenoron","Anthemis","Anthodiscus","Anthopogon","Anthoxanthum","Anthriscus","Anthyllis","Anticlea","Antidaphne","Antirrhinum","Anychia","Apeiba","Apera","Aphanostephus","Aphelandra","Aphyllon","Apios","Aplectrum","Aploppapus","Apocynum","Apogon","Aptandropsis","Aquilegia","Arabidopsis","Arabis","Arachis","Aragallus","Aralia","Araucaria","Arbutus","Arceuthobium","Archibaccharis","Arctagrostis","Arctium","Arctostaphylos","Ardisia","Arenaria","Arenga","Arethusa","Argemone","Argentacer","Argentina","Arisaema","Aristida","Aristolochia","Armoracia","Arnica","Arnoglossum","Arnoseris","Aronia","Arrabidaea","Arrhenatherum","Artemisia","Arthrostylidium","Arum","Aruncus","Arundinaria","Asarum","Asclepias","Ascyrum","Asimina","Asparagus","Asperella","Asperula","Aspidium","Aspidosperma","Aspilia","Asplenium","Aster","Astragalus","Astranthium","Astrocaryum","Astronia","Astronidium","Astronium","Ateleia","Atelophragma","Athenaea","Atheropogon","Athyrium","Atractantha","Atragene","Atriplex","Atropa","Attalea","Aubrieta","Aulonemia","Aureolaria","Austroeupatorium","Aveledoa","Avena","Avenula","Avicennia","Ayapanopsis","Ayenia","Azalea","Azolla","Baccaurea","Baccharis","Bacopa","Bactris","Baeothryon","Baileya","Bakeridesia","Balaka","Balanites","Balanopaceae","Ballota","Balmea","Balsamita","Balsamorhiza","Baltimora","Banksia","Baptisia","Barbarea","Barnadesia","Barringtonia","Bartlettina","Bartonia","Bartsia","Bassavia","Bassia","Bassovia","Batesimalva","Bathysa","Batis","Batrachium","Batschia","Bauhinia","Bealia","Beckmannia","Begonia","Beilschmiedia","Belamcanda","Bellis","Beloperone","Benthamia","Berberis","Berchemia","Berlandiera","Bernardia","Berteroa","Berula","Besleria","Bessera","Besseya","Betula","Bicuculla","Bidens","Bifolium","Bignonia","Bilderdykia","Bistorta","Blakea","Blennosperma","Blephariglottis","Blepharoneuron","Blephilia","Blitum","Bocoa","Boebera","Boechera","Boehmeria","Bolanosa","Bolboschoenus","Boltonia","Bomarea","Bonamia","Borago","Borreria","Bothriochloa","Botrychium","Botrydium","Bougainvillea","Bourreria","Bouteloua","Bouvardia","Brachiaria","Brachiolobos","Brachistus","Brachyactis","Brachyelytrum","Brachyotum","Bradburia","Bramia","Brasenia","Brasiliocroton","Brassica","Brauneria","Bravaisia","Braxilia","Braya","Brexiella","Brickellia","Briquetia","Briza","Brodiaea","Bromelica","Bromopsis","Bromus","Brosimopsis","Brosimum","Brownea","Brunellia","Brunfelsia","Bruniera","Bryonia","Brysonima","Buccaferrea","Buchanania","Buchenavia","Buchloe","Buchnera","Buddleja","Buglossoides","Bulbilis","Bulbostylis","Bumelia","Bunchosia","Bunias","Buphthalmum","Bupleurum","Burmeistera","Bursa","Bursera","Burshia","Butomus","Byrsonima","Byttneria","Cabomba","Cacalia","Cactus","Caesalpinia","Caesalpiniodes","Caex","Cakile","Calamagrostis","Calamintha","Calamovilfa","Calathea","Calatola","Calceolaria","Calderonia","Calendula","Calispepla","Calla","Callaeum","Calliandra","Callicarpa","Calliopsis","Callirhoe","Callistemon","Callistephus","Callitriche","Calluna","Calochortus","Caloncoba","Calophyllum","Calopogon","Calothamnus","Caltha","Calycadenia","Calycanthus","Calycodendron","Calycogonium","Calycophyllum","Calylophus","Calypso","Calyptranthes","Calyptridium","Calystegia","Calytrix","Camassia","Camelina","Camellia","Campanula","Campanulastrum","Campe","Campomanesia","Campsis","Camptosorus","Canadanthus","Canarium","Canavalia","Cannabis","Canthium","Caopia","Capnoides","Capparis","Capsella","Capsicum","Caragana","Carapa","Carara","Cardamine","Cardaria","Cardiospermum","Carduus","Carex","Cariniana","Carpinus","Carpodiptera","Carpotroche","Carthamus","Carum","Carya","Caryocar","Caryodaphnopsis","Caryodendron","Caryota","Casearia","Cashalia","Cassandra","Cassia","Cassipourea","Castalia","Castanea","Castilleja","Catabrosa","Catabrosella","Catachaenia","Catalpa","Catapodium","Cathartolinum","Cathea","Catostemma","Caulinia","Caulophyllum","Cavendishia","Cayaponia","Ceanothus","Cecropia","Cedrela","Ceiba","Celastrus","Celiantha","Celosia","Celtis","Cenchrus","Centaurea","Centaurium","Centrochloa","Centrolobium","Centropogon","Centunculus","Cephalanthus","Cephalaria","Cerastium","Cerasus","Ceratocephala","Ceratocephalus","Ceratophyllum","Ceratostema","Ceratoxalis","Cercis","Cercocarpus","Cervantesia","Cespa","Cestrum","Chaenactis","Chaenomeles","Chaenorhinum","Chaerophyllum","Chaetochloa","Chaetogastra","Chaetopappa","Chaiturus","Chamaecrista","Chamaedaphne","Chamaefistula","Chamaelirium","Chamaepericlymenum","Chamaerhodos","Chamaesaracha","Chamaesyce","Chamerion","Chamomilla","Charpentiera","Chasmanthium","Chassalia","Cheilanthes","Cheiloclinium","Cheiranthus","Cheirinia","Cheirodendron","Chelidonium","Chelone","Chenopodium","Chidlowia","Chilopsis","Chimaphila","Chimarrhis","Chiogenes","Chlonanthus","Chloris","Chlorocrepis","Chlorocyperus","Chloroleucon","Chlorophora","Choisya","Chomelia","Chondrosum","Chorizanthe","Chrysanthemum","Chrysochlamys","Chrysocoma","Chrysophyllum","Chrysopsis","Chrysosplenium","Chrysothamnus","Chusquea","Chytroma","Cicer","Cichorium","Cicuta","Cienfuegosia","Cimicifuga","Cinchona","Cinna","Cinnamomum","Cipura","Circaea","Cirsium","Cissus","Cistus","Citharexylum","Citronella","Citrullus","Cladium","Cladocolea","Cladorhiza","Cladrastis","Claoxylon","Clarkia","Clathrotropis","Clavija","Claytonia","Cleidion","Cleistocalyx","Clematis","Cleome","Clethra","Clidemia","Cliftonia","Climacoptera","Clinopodium","Clintonia","Clusia","Clypeola","Clytostoma","Cnicus","Cnidoscolus","Cobana","Coccoloba","Coccothrinax","Cocculus","Cochlearia","Coeloglossum","Cohniella","Cola","Colea","Coleogeton","Colicodendron","Collinsia","Collinsonia","Collomia","Colubrina","Columnea","Coluteocarpus","Comandra","Comarum","Combretum","Commelina","Compsoneura","Comptonia","Conceveiba","Condalia","Conioselinum","Conium","Connarus","Conomorpha","Conopholis","Conospermum","Conostegia","Conradina","Conringia","Consolida","Convallaria","Convolvulus","Conyza","Conzattia","Copaifera","Coprosma","Coprosmanthus","Coptis","Corallorhiza","Cordia","Cordylanthus","Coreopsis","Coriandrum","Coriflora","Corispermum","Cornella","Cornucopiae","Cornus","Cornutia","Coronaria","Coronilla","Coronopus","Corydalis","Corylus","Coryphantha","Corythophora","Cosmos","Costus","Cota","Cotinus","Cotoneaster","Cotopaxia","Couepia","Couma","Couratari","Couroupita","Coursetia","Coussapoa","Coussarea","Cracca","Crassula","Crataegus","Crepis","Crescentia","Crinodendron","Criosanthes","Cristatella","Critesion","Critonia","Crocanthemum","Crocosmia","Crocus","Crossopetalum","Crossostylis","Crotalaria","Croton","Crotonopsis","Crudia","Crypsis","Crypta","Cryptantha","Cryptocarya","Cryptochloa","Cryptogramma","Cryptotaenia","Cuatresia","Cubelium","Cucubalus","Cucumis","Cucurbita","Cunila","Cupania","Cupaniopsis","Cuphea","Cupressus","Cuscuta","Cyanea","Cyanococcus","Cyanotris","Cyathocalyx","Cybianthus","Cyclachaena","Cyclolepis","Cycloloma","Cyclopogon","Cylactis","Cylindropuntia","Cymbalaria","Cymbidium","Cymbopetalum","Cymopterus","Cynanchum","Cynodon","Cynoglossum","Cynometra","Cynosurus","Cynthia","Cypella","Cyperus","Cyphomandra","Cypripedium","Cyrtandra","Cyrtorrhyncha","Cystium","Cystopteris","Cytherea","Cytisus","Dacrydium","Dacryodes","Dactylis","Dahlia","Dalbergaria","Dalbergia","Dalea","Dalibarda","Danthonia","Daphne","Daphnopsis","Darmera","Dasiphora","Dasistoma","Dasylirion","Dasystephana","Datisca","Datura","Daucus","Daviesia","Davilla","Decachaena","Decemium","Decodon","Delopyrum","Delostoma","Delphinium","Demidovia","Demosthenesia","Dendranthema","Dendropanax","Dendrophthora","Dendrostigma","Dennstaedtia","Denslovia","Dentaria","Deparia","Deprea","Deringa","Derris","Deschampsia","Descurainia","Desmanthus","Desmazeria","Desmodium","Desmopsis","Desmos","Deutzia","Dhofaria","Dialyanthera","Dianthera","Dianthus","Diarina","Diarrhena","Dicanthelium","Dicentra","Dicerandra","Dichaea","Dichanthelium","Dichapetalum","Dichondra","Dichostylis","Dichromena","Dichrophyllum","Diclidium","Diclinanona","Dicliptera","Dicymbe","Didelotia","Didiplis","Dierama","Diervilla","Digitalis","Digitaria","Dillenia","Dillwynia","Dimorphandra","Dimorphanthus","Dimorphocarpa","Diodella","Diodia","Dioscorea","Diospyros","Diphasiastrum","Diphasium","Dipholis","Diphryllum","Diplachne","Diplacus","Diplazium","Diplopappus","Diplostephium","Diplotaxis","Dipsacus","Dipterocarpus","Dirca","Discophora","Disporum","Distegia","Distichlis","Ditassa","Ditaxis","Ditremexa","Dodecatheon","Doellingeria","Dolichos","Doliocarpus","Dombeya","Dondia","Doronicum","Draba","Dracaena","Dracocephalum","Dracontium","Drosera","Dryandra","Dryas","Drymaria","Drymocallis","Drymonia","Dryopteris","Drypetes","Duabanga","Dubautia","Duchesnea","Duguetia","Dulichium","Dunalia","Duschekia","Dysphania","Dyssodia","Eatonia","Echeandia","Echinacea","Echinocereus","Echinochloa","Echinocystis","Echinodorus","Echinops","Echinospermum","Echites","Echium","Eclipta","Egeria","Eichhornia","Elaeagia","Elaeagnus","Elaeocarpus","Elaphoglossum","Elatine","Elattostachys","Eleocharis","Elephantopus","Eleusine","Eleutherine","Eleutherococcus","Elizabetha","Elleanthus","Ellisia","Elodea","Elsholtzia","Elymus","Elytrigia","Emelista","Empetrum","Encelia","Encyclia","Endiandra","Endospermum","Enemion","Eperua","Ephedra","Ephedranthus","Ephemerum","Epidendrum","Epifagus","Epigaea","Epilobium","Epipactis","Equisetum","Eragrostis","Erechtites","Eremostachys","Eriastrum","Ericameria","Erigenia","Erigeron","Eriocaulon","Eriochloa","Eriocoma","Eriogonum","Erioneuron","Eriophorum","Eriophyllum","Erodium","Erophila","Errazurizia","Erucastrum","Erxlebenia","Erycibe","Eryngium","Erysimum","Erythrina","Erythrocoma","Erythrodes","Erythronium","Erythroxylum","Eschscholzia","Eschweilera","Escobaria","Esenbeckia","Espeletia","Eucalyptus","Euchlaena","Eugenia","Eumorphanthus","Euonymus","Eupatoriadelphus","Eupatorium","Euphorbia","Euphrasia","Euplassa","Eurbia","Eurya","Eurybia","Eurydochus","Eustoma","Euterpe","Euthamia","Evactoma","Evolvulus","Evonymus","Excavatia","Facelia","Fagara","Fagelia","Fagopyrum","Fagus","Fagus-Castanea","Falcaria","Falcata","Fallopia","Fallugia","Faramea","Fatoua","Fedia","Fendlera","Fendlerella","Fernandoa","Ferula","Festuca","Ficus","Filaginella","Filago","Filipendula","Filix","Fimbristylis","Fischeria","Fissipes","Fissistigma","Flacourtia","Flaveria","Fleischmannia","Floerkea","Fluckigeria","Fluvialis","Foeniculum","Forestiera","Forsellesia","Forsteronia","Forsythia","Fosteria","Fouquieria","Fragaria","Frangula","Frankenia","Franseria","Frasera","Fraxinus","Freessoa","Fremontodendron","Fritillaria","Froelichia","Fuchsia","Fuirena","Fumaria","Funastrum","Funtumia","Gaertnera","Gaillardia","Gaillarida","Galactia","Galactophora","Galarhoeus","Gale","Galearis","Galeopsis","Galeorchis","Galinsoga","Galium","Galphimia","Galypola","Gamochaeta","Garcinia","Gardenia","Garrya","Gaultheria","Gaura","Gaylussacia","Gayophytum","Geissanthus","Geissospermum","Gemmingia","Genipa","Genista","Gentiana","Gentianella","Gentianopsis","Geocaulon","Geonoma","Geoprumnon","Geranium","Gerardia","Gesneria","Geum","Gilia","Gilibertia","Gillespiea","Ginkgo","Githopsis","Glandularia","Glaucium","Gleasonia","Glechoma","Gleditsia","Glochidion","Gloxinia","Glyceria","Glycine","Glycyrrhiza","Gnaphaliothamnus","Gnaphalium","Gonolobus","Gonzalagunia","Goodyera","Gothofreda","Gouldia","Graffenrieda","Grammadenia","Grammica","Graphephorum","Gratiola","Greeneocharis","Grevillea","Grewia","Grias","Grindelia","Grossularia","Guadua","Guaiacum","Guapira","Guarea","Guatteria","Guazuma","Guettarda","Guilandina","Guioa","Guizotia","Gustavia","Gutierrezia","Gymnadeniopsis","Gymnandra","Gymnocarpium","Gymnocladus","Gymnopogon","Gynoxys","Gypsophila","Gyrostachys","Habenaria","Habracanthus","Hackelia","Haematoxylum","Hagsatera","Hakea","Halenia","Halerpestes","Halimium","Hamamelis","Hamelia","Hampea","Haploclathra","Haplopappus","Hasteola","Hauya","Hebeclinium","Hecastocleis","Hecatonia","Hedeoma","Hedera","Hedstromia","Hedyosmum","Hedyotis","Hedysarum","Heisteria","Helenium","Heleochloa","Helianthemum","Helianthopsis","Helianthus","Heliconia","Helicostylis","Helicteres","Helicteropsis","Helictotrichon","Heliocarpus","Heliopsis","Heliotropium","Helleborine","Helleborus","Helmiopsiella","Helogyne","Helonias","Helothrix","Hemerocallis","Hemicarpha","Hemitelia","Hemizonia","Hendecandras","Henriettea","Henriettella","Hepatica","Heracleum","Hernandia","Herniaria","Herrania","Hesperis","Hesperomannia","Hesperostipa","Heteranthera","Heteropterys","Heterospathe","Heterotheca","Heuchera","Hevea","Hexalectris","Hexastylis","Hibiscadelphus","Hibiscus","Hicoria","Hieracium","Hierochloe","Hieronyma","Hilaria","Himantostemma","Himatanthus","Hippochaete","Hippocratea","Hippophae","Hipposelinum","Hippuris","Hiptage","Hirtella","Hoffmannia","Hoffmannseggia","Holcus","Holocarpha","Holodiscus","Holographis","Holosteum","Holtonia","Homalium","Homalocenchrus","Homalosorus","Hordeum","Horkelia","Hornschuchia","Horsfordia","Hortia","Hosackia","Hosta","Houstonia","Hudsonia","Hugonia","Humberodendron","Humbertiella","Humiria","Humiriastrum","Humulus","Huperzia","Hura","Hyacinthoides","Hyacinthus","Hybanthus","Hydrangea","Hydranthelium","Hydrastis","Hydrilla","Hydrocharis","Hydrocleis","Hydrocotyle","Hydrophyllum","Hylocarpa","Hylotelephium","Hymenaea","Hymenoclea","Hymenolobium","Hymenopappus","Hymenophysa","Hymenoxys","Hyoscyamus","Hyoseris","Hyperacanthus","Hyperbaena","Hypericum","Hypochaeris","Hypogomphia","Hypopitys","Hypoxis","Hyptis","Hyssopus","Hystrix","Iberis","Ibidium","Icacorea","Ilex","Iliamna","Ilysanthes","Impatiens","Indigofera","Inga","Inula","Iochroma","Iodanthus","Ionactis","Ionoxalis","Ioxylon","Ipomoea","Ipomopsis","Iresine","Iris","Iryanthera","Isachne","Isanthus","Isatis","Isertia","Isnardia","Isocoma","Isoetes","Isolepis","Isolona","Isopogon","Isopyrum","Isotrema","Isotria","Iva","Ivesia","Ixora","Jacquemontia","Jacqueshuberia","Jaegeria","Jahnia","Jaltomata","Janusia","Jatropha","Jeffersonia","Joosia","Jovibarba","Juglans","Juncoides","Juncus","Jungia","Juniperus","Jupunba","Jussiaea","Justicia","Kadua","Kalmia","Kalmiopsis","Kalopanax","Karomia","Kaunia","Kermadecia","Kickxia","Kiggelaria","Klarobelia","Knautia","Kneiffia","Koanophyllon","Kobresia","Kochia","Koeleria","Koellia","Koniga","Korthalsella","Korycarpus","Kosteletzkya","Krameria","Krascheninnikovia","Krigia","Kuhnia","Kuhnistera","Kummerowia","Kunzea","Kyllinga","Kyrstenia","Lablab","Lachnanthes","Lachnocaulon","Lachnostachys","Lacinaria","Lacistema","Lacmellea","Lactuca","Ladenbergia","Laetia","Lagophylla","Laguncularia","Lambertia","Lamium","Lamourouxia","Lamprocapnos","Langloisia","Lantana","Laphamia","Laportea","Lappa","Lappula","Lapsana","Larix","Larnax","Larrea","Lasallea","Lasiacis","Lastrea","Lathyrus","Laurus","Laxoplumeria","Layia","Leandra","Leavenworthia","Lechea","Lecticula","Lecythis","Ledum","Leea","Leersia","Legousia","Lemna","Lens","Leonia","Leontice","Leontodon","Leonurus","Lepachys","Lepadena","Lepanthes","Lepargyrea","Lepechinia","Lepechiniella","Lepidanthus","Lepidium","Lepidotheca","Lepidotis","Lepigonum","Leptamnium","Leptandra","Leptilon","Leptochloa","Leptodactylon","Leptoglottis","Leptoloma","Leptopharynx","Leptorchis","Lerchenfeldia","Lespedeza","Lesquerella","Lettowianthus","Leucacantha","Leucanthemella","Leucanthemum","Leucocoma","Leucocrinum","Leucojum","Leucophyllum","Leucophysalis","Leucospora","Levisticum","Lewisia","Lexarzanthe","Leymus","Liabum","Liatris","Licania","Licaria","Ligusticum","Ligustrum","Lilium","Limnanthemum","Limnobotrya","Limnorchis","Limodorum","Limonium","Limosella","Linaria","Lindera","Lindernia","Lindleya","Linnaea","Linociera","Linum","Liparis","Lipocarpha","Lipochaeta","Lippia","Liquidambar","Liquidamber","Liriodendron","Lisianthius","Listera","Lithocarpus","Lithophragma","Lithospermum","Litsea","Littorella","Llagunoa","Lobelia","Lobularia","Loeselia","Logfia","Lolium","Lomatium","Lonchocarpus","Lonicera","Lophanthera","Lophanthus","Lophiaris","Lophopappus","Lophospermum","Lophotocarpus","Loreya","Lorostemon","Lotus","Louteridium","Loxopterygium","Loxothysanus","Lubaria","Lucuma","Ludwigia","Lueheopsis","Lunaria","Lupinus","Luzula","Lychnis","Lycianthes","Lycium","Lycopersicon","Lycopodiella","Lycopodium","Lycopsis","Lycopus","Lycoseris","Lygistum","Lygodesmia","Lyonia","Lysias","Lysiella","Lysimachia","Lysionotus","Lythrum","Maba","Macaranga","Machaeranthera","Machaerium","Macleania","Maclura","Macrocarpaea","Macrolobium","Macromeria","Macrostelia","Macuillamia","Madia","Magnolia","Mahonia","Mahurea","Maianthemum","Malachium","Malacothamnus","Malaxis","Malcolmia","Malouetia","Malpighia","Malus","Malva","Malvastrum","Malvaviscus","Mammea","Mandevilla","Manettia","Manfreda","Mangifera","Manihot","Manilkara","Maniltoa","Mannagettaea","Mapourea","Mappia","Maprounea","Maquira","Marah","Maranta","Marcocarpaea","Margaritaria","Mariana","Marila","Mariscus","Marlierea","Marrubium","Marsdenia","Marsilea","Martiodendron","Martiusia","Maruta","Matayba","Matelea","Matisia","Matricaria","Matteuccia","Maxillaria","Mayna","Maytenus","Mazus","Medeola","Medicago","Medinilla","Megalodonta","Megistostegium","Meibomia","Melaleuca","Melampodium","Melampyrum","Melandrium","Melanoxylum","Melanthium","Melchiora","Melica","Melicoccus","Melicope","Melilotus","Meliosma","Melissa","Melochia","Mendoncia","Menispermum","Menodora","Mentha","Mentzelia","Menyanthes","Meriania","Meriolix","Merostachys","Merremia","Mertensia","Mesadenia","Mespilus","Mesynium","Metalepis","Metastelma","Metopium","Metrosideros","Miconia","Micrampelis","Micrandra","Micranthes","Microcos","Micromeria","Micropholis","Microseris","Microspermum","Microstegium","Microstylis","Microtropis","Mikania","Milium","Milla","Millettia","Mimosa","Mimulus","Mimusops","Minuartia","Minuopsis","Mirabilis","Miscanthus","Mitchella","Mitella","Mitropsidium","Moehringia","Moldavica","Molinia","Mollugo","Monarda","Monardella","Moneses","Moniera","Monilistus","Monnina","Monochaetum","Monolepis","Monolopia","Monotropa","Montanoa","Montia","Mooria","Moquilea","Mora","Morinda","Morisonia","Morocarpus","Moronobea","Mortoniodendron","Morus","Mosannona","Mouriri","Mouriria","Muhlenbergia","Mulgedium","Munnozia","Munroa","Muntingia","Muricauda","Muscari","Musgravea","Musineon","Mutisia","Myagrum","Myosotis","Myosoton","Myosurus","Myrcia","Myrcianthes","Myrciaria","Myrica","Myriocarpa","Myriophyllum","Myristica","Myrrhis","Myrteola","Mystroxylon","Myzorrhiza","Nabalus","Najas","Nama","Napaea","Narcissus","Nardosmia","Narthecium","Narukila","Nasmythia","Nassella","Nasturtium","Naumburgia","Nautilocalyx","Nectandra","Neea","Negundo","Nelsonianthus","Nelumbium","Nelumbo","Nemastylis","Nemexia","Nemopanthus","Nemophila","Neobeckia","Neocuatrecasia","Neolepia","Neosprucea","Neottia","Nepeta","Nephrodium","Neptunia","Neslia","Neviusia","Nezera","Nicandra","Nicotiana","Nintooa","Nolina","Norta","Northia","Nothocalais","Notholaena","Nothoscordum","Nuphar","Nuttalanthus","Nuttallanthus","Nuttallia","Nyctelea","Nymphaea","Nymphoides","Nymphozanthus","Nyssa","Oakesia","Oakesiella","Obeliscaria","Oberna","Obolaria","Ochis","Ochroma","Ochthocosmus","Ocimum","Oclemena","Ocotea","Odontites","Oedematopus","Oemleria","Oenanthe","Oenocarpus","Oenothera","Oerstedianthus","Oglifa","Oldenlandia","Olea","Oligactis","Oligoneuron","Oligosporus","Olmedia","Olsynium","Olyra","Omalotheca","Onagra","Oncidium","Onobrychis","Onoclea","Ononis","Onopordum","Onoseris","Onosma","Onosmodium","Onychopetalum","Ophiocephalus","Ophiocolea","Ophioglossum","Ophioscorodon","Ophrys","Oplopanax","Oplotheca","Opulaster","Opuntia","Orbexilum","Orchis","Oregandra","Oreocarya","Oreopanax","Origanum","Ormosia","Ornithogalum","Orobanche","Orobus","Orontium","Orthilia","Orthocarpus","Oryctanthus","Oryzopsis","Osmaronia","Osmorhiza","Osmunda","Ossaea","Ostrya","Ostryoderris","Otatea","Othake","Otophylla","Ouratea","Oxalis","Oxybaphus","Oxycoccus","Oxypetalum","Oxypolis","Oxyria","Oxytropis","Oyedaea","Pachira","Pachistima","Pachysandra","Packera","Padus","Paeonia","Paepalanthus","Pagiantha","Paivaeusa","Palafoxia","Palicourea","Panax","Pandanus","Panicularia","Panicum","Panopsis","Papaver","Pappobolus","Pappophorum","Paraclarisia","Paradrymonia","Paramachaerium","Paraprotium","Parathelypteris","Parathesis","Pariana","Parietaria","Parinari","Parmentiera","Parnassia","Paronychia","Paropsia","Parosela","Parthenium","Parthenocissus","Pascopyrum","Paspalum","Passerina","Passiflora","Pastinaca","Paullinia","Paulownia","Pausandra","Pavonia","Pectis","Pedicularis","Pediomelum","Peiranisia","Pelargonium","Pellaea","Peltaea","Peltandra","Peltastes","Peltiphyllum","Peltogyne","Peltostigma","Pennisetum","Penstemon","Pentacalia","Pentaclethra","Pentagonia","Pentapanax","Pentaphylloides","Pentaplaris","Pentaspadon","Penthorum","Peperomia","Peplis","Pepo","Pera","Perama","Peramium","Peraphyllum","Perebea","Pereskia","Perezia","Periblema","Perideridia","Perilla","Periptera","Perispermum","Perissocarpa","Perissocoeleum","Perityle","Perotis","Perrierophytum","Persea","Persica","Persicaria","Perymenium","Petalostemon","Petasites","Petrea","Petrophile","Petrorhagia","Petunia","Phaca","Phacelia","Phaeocephalum","Phalaris","Phalaroides","Phaleria","Pharbitis","Pharus","Phaseolus","Phegopteris","Phellodendron","Phelypaea","Phemeranthus","Philadelphus","Philodendron","Philoglossa","Philotria","Phippsia","Phleum","Phloiodicarpus","Phlox","Phoebe","Phoradendron","Photinia","Phragmites","Phragmotheca","Phryma","Phthirusa","Phyla","Phyllanthus","Phyllarthron","Phylloctenium","Physalis","Physalodes","Physaria","Physocarpus","Physostegia","Phyteuma","Phytolacca","Picea","Picramnia","Pilea","Pilocarpus","Pimenta","Pimpinella","Pinguicula","Pinus","Piper","Piperia","Piptatherum","Piptocarpha","Piptochaetium","Piqueriopsis","Piratinera","Piresia","Pisonia","Pistia","Pisum","Pitcairnia","Pithecellobium","Pittocaulon","Plagiobothrys","Plananthus","Plantago","Platanthera","Platanus","Platycodon","Platymiscium","Pleiotaenia","Pleonotoma","Pleopeltis","Plerandra","Pleuropterus","Pleurothallis","Plinia","Pluchea","Plumeria","Plummera","Pneumonanthe","Poa","Pochota","Podocarpus","Podophyllum","Podostemum","Pogonia","Poinsettia","Polanisia","Polemonium","Polianthes","Poliomintha","Pollalesta","Pollinirhiza","Polyalthia","Polycnemum","Polygala","Polygonatum","Polygonella","Polygonum","Polymnia","Polypodium","Polypogon","Polystichum","Polytaenia","Ponerorchis","Pontederia","Ponthieva","Populus","Porophyllum","Porteranthus","Portulaca","Potamogeton","Potentilla","Pourouma","Pouteria","Pradosia","Premna","Prenanthes","Prestoea","Prestonia","Primula","Pringleophytum","Prinos","Prionosiadium","Pristimera","Proboscidea","Proserpinaca","Prosopis","Prosthechea","Protium","Prunella","Prunus","Psammophiliella","Psedera","Pseuderanthemum","Pseudocaryophyllus","Pseudoconnarus","Pseudognaphalium","Pseudokyrsteniopsi","Pseudomalmea","Pseudoroegneria","Pseudotsuga","Pseudoxandra","Psidium","Psilocarya","Psilostrophe","Psittacanthus","Psoralea","Psoralidium","Psychopterys","Psychotria","Psyllocarpus","Ptelea","Pteretis","Pteridium","Pteris","Pterocarpus","Pterospora","Pterotropia","Pterygota","Ptilimnium","Ptychosperma","Puccinellia","Pueraria","Pulmonaria","Pulsatilla","Purshia","Puya","Pycnanthemum","Pycreus","Pyrethrum","Pyrola","Pyrrhopappus","Pyrus","Quamasia","Quamoclit","Quapoya","Quararibea","Quassia","Quercus","Quiina","Raddia","Radicula","Rahowardiana","Railliardia","Raimannia","Ramischia","Randia","Ranunculus","Rapanea","Raphanus","Rapistrum","Ratibida","Rauvolfia","Ravenia","Raveniopsis","Razoumofskya","Readea","Recordoxylon","Reevesia","Regelia","Rehdera","Reichenbachia","Remijia","Reseda","Reynoutria","Rhamnidium","Rhamnus","Rheedia","Rheum","Rhexia","Rhigozum","Rhinanthus","Rhipidocladum","Rhizophora","Rhodiola","Rhodocolea","Rhododendron","Rhodostemonodaphne","Rhodotypos","Rhopalocarpus","Rhus","Rhynchospora","Ribes","Richeria","Ricinodendron","Ridan","Rigidella","Rinorea","Robertiella","Robinia","Rochelia","Roegneria","Roldana","Rollinia","Romanschulzia","Rondeletia","Rorippa","Rosa","Rotala","Rouliniella","Roupala","Roystonea","Ruagea","Rubacer","Rubus","Rudbeckia","Rudgea","Ruellia","Rufacer","Rumex","Ruppia","Ruprechtia","Rusbyanthus","Russelia","Ruta","Ryania","Sabatia","Sabicea","Sabina","Sabulina","Saccharodendron","Sacoglottis","Sagina","Sagittaria","Salacia","Salicornia","Salix","Salmea","Salpichroa","Salsola","Salvia","Sambucus","Samolus","Sanguinaria","Sanguisorba","Sanicula","Santolina","Sapindus","Sapium","Saponaria","Saracha","Sarcostemma","Sarothra","Sarracenia","Sassafras","Satureja","Satyria","Satyrium","Saurauia","Saururus","Saussurea","Savastana","Saxifraga","Saxofridericia","Scabiosa","Scaevola","Scalesia","Scaphyglottis","Schaefferia","Schedonnardus","Schefflera","Scheuchzeria","Schiedea","Schizachne","Schizachyrium","Schizanthus","Schizocarpum","Schizonotus","Schizostege","Schlegelia","Schmaltzia","Schobera","Schoenocaulon","Schoenolirion","Schoenoplectus","Schoenus","Schollera","Schrankia","Sciadodendron","Scilla","Scirpus","Scleranthus","Scleria","Sclerolobium","Scleropoa","Scleropogon","Scoliopus","Scolochloa","Scrophularia","Scutellaria","Sebastiania","Secale","Sechium","Securigera","Sedum","Seemannia","Selaginella","Sempervivum","Senecio","Senegalia","Senna","Serapias","Sericocarpus","Serinia","Serjania","Serratula","Sesamum","Sesbania","Sesleria","Sessea","Sessilanthera","Setaria","Setiscapella","Seymeria","Shepherdia","Sherardia","Sibara","Sibbaldiopsis","Sickingia","Sicyos","Sida","Sidalcea","Sideritis","Sideroxylon","Siella","Sieversia","Silene","Silphium","Silybum","Simaba","Simarouba","Simsia","Sinapis","Siparuna","Siphocampylus","Sisymbrium","Sisyrinchium","Sitanion","Sium","Sloanea","Smilacina","Smilax","Smyrnium","Soja","Solanum","Solidago","Sonchus","Sophia","Sophora","Sorbaria","Sorbus","Sorghastrum","Sorghum","Sorhum","Sorocea","Souroubea","Sparattanthelium","Sparganium","Spartina","Spathyema","Specularia","Spergula","Spergularia","Spergulastrum","Spermolepis","Sphacele","Sphaeralcea","Sphaeranthus","Sphaerophysa","Sphagnum","Sphenopholis","Sphenostigma","Spigelia","Spilanthes","Spiraea","Spiranthes","Spirodela","Spondias","Sporobolus","Sprekelia","Stachys","Stachytarpheta","Stahlia","Stanleya","Staphylea","Stegolepis","Steiractina","Steironema","Stelis","Stellaria","Stemmadenia","Stemmodontia","Stemodia","Stemodiacra","Stenactis","Stenanona","Stenanthera","Stenogyne","Stenopadus","Stenophyllus","Stenotus","Stephanomeria","Steptopus","Sterculia","Stereospermum","Sterigmapetalum","Stevia","Stigmaphyllon","Stipa","Stomoisia","Streptocalyx","Streptocarpus","Streptopus","Strigosella","Striolaria","Strobus","Stroganowia","Strophocaulos","Strophostyles","Struthanthus","Struthiopteris","Strychnos","Stuckenia","Stylogyne","Stylophorum","Stylosanthes","Stylypus","Suaeda","Subularia","Sullivantia","Swainsona","Swartzia","Swertia","Swida","Swietenia","Sycocarpus","Symbolanthus","Symphonia","Symphoricarpos","Symphyotrichum","Symphytum","Symplocarpus","Symplocos","Synaphea","Synardisia","Syndesmon","Syngonanthus","Synosma","Syntherisma","Synthyris","Syringa","Syzygium","Tabebuia","Tabernaemontana","Tachigali","Tacsonia","Taenidia","Tagetes","Talauma","Talinum","Talipariti","Tamarix","Tanacetopsis","Tanacetum","Tapirira","Tapura","Taraxacum","Taxodium","Taxus","Tecoma","Tectaria","Tectona","Telipogon","Teloxys","Tephrosia","Terminalia","Ternstroemia","Terrellia","Terrelymus","Tetraclea","Tetradymia","Tetragastris","Tetragonia","Tetraneuris","Tetraplasandra","Tetrapterys","Tetrorchidium","Teucrium","Thacla","Thalesia","Thalictrum","Thamnosma","Thaspium","Thelesperma","Thelypodium","Thelypteris","Themistoclesia","Theobroma","Thermia","Thermopsis","Thesium","Thespesia","Thibaudia","Thlaspi","Thompsonella","Thouinia","Thrasya","Thryptomene","Thuja","Thymelaea","Thymophylla","Thymus","Thysanella","Tiarella","Tigridia","Tilia","Tillandsia","Timonius","Tiniaria","Tiquilia","Tissa","Tithymalopsis","Tithymalus","Tococa","Tofieldia","Tomanthera","Tonestus","Torilis","Torresea","Torresia","Torreyochloa","Torrubia","Torulinium","Tournefortia","Tovara","Tovaria","Tovomita","Tovomitopsis","Townsendia","Toxicodendron","Toxylon","Tracaulon","Tradescantia","Tragia","Tragopogon","Trapa","Trattinnickia","Trautvetteria","Triadenum","Triantha","Tribulus","Trichelostylis","Trichilia","Trichogonia","Trichophorum","Trichophyllum","Trichoscypha","Trichosporum","Trichostema","Triclinium","Triclisperma","Tricyrtis","Tridens","Trientalis","Trifolium","Triglochin","Trigonella","Trigonostemon","Trigyneia","Trillium","Trilopus","Trimorpha","Triodanis","Triodia","Triodon","Trionum","Triosteum","Triphora","Triplaris","Triplasis","Tripleurospermum","Tripolium","Tripsacum","Trisetum","Triteleia","Triticum","Trixis","Trophis","Troximon","Truellum","Tsuga","Tulipa","Tunica","Turritis","Tussilago","Tutcheria","Typha","Udora","Ulmaria","Ulmus","Unamia","Ungnadia","Unifolium","Uniola","Unisema","Unonopsis","Urena","Uribea","Uropappus","Urostachys","Urtica","Urticastrum","Urvillea","Utricularia","Uvaria","Uva-Ursi","Uvularia","Vaccaria","Vaccinium","Vachellia","Vagnera","Valeriana","Valerianella","Validallium","Vallea","Vallisneria","Vantanea","Vassobia","Vatairea","Vavaea","Ventenata","Veratrum","Verbascum","Verbena","Verbesina","Vernonia","Veronica","Veronicastrum","Vesiculina","Viburnum","Vicia","Viguiera","Vilfa","Villadia","Vinca","Vincetoxicum","Vinticena","Viola","Viorna","Virgulus","Virola","Vismia","Vitex","Vitiphoenix","Vitis","Vittaria","Vochysia","Vouacapoua","Vriesea","Vulpia","Waldsteinia","Wallacea","Wallia","Wallichia","Warszewiczia","Washingtonia","Weberaster","Weberbauera","Wedila","Weigeltia","Wenzelia","Westringia","Wikstroemia","Willoughbya","Wimmeria","Windsoria","Wissadula","Wisteria","Wolffia","Wolffiella","Woodsia","Woodwardia","Wormia","Wulfenia","Wyethia","Xanthium","Xanthosia","Xanthoxalis","Xanthoxylum","X","Asplenosorus","Ximenia","X","Sorbaronia","Xylia","Xylopia","Xylosma","Xylosteon","Xylosteum","Xyris","Yucca","Zannichellia","Zanthoxylum","Zauschneria","Zea","Zephyranthes","Zexmenia","Zigadenus","Zinnia","Zizania","Zizia","Ziziphora","Ziziphus","Zosterella","Zuelania","Zygia","Zygophyllidium"]


#genusList was obtained like this:
# SELECT DISTINCT genus FROM spdetail WHERE Syncd='.' AND Wisc_Found='W'
genusList = ["Abies","Abutilon","Acalypha","Acer","Achnatherum","Achillea","Acinos","Acorus","Agastache","Agalinis","Alnus","Alopecurus","Ampelopsis","Aconitum","Actaea","Adenocaulon","Adiantum","Adlumia","Adoxa","Aegopodium","Aesculus","Aethusa","Agrostis","Agropyron","Agrimonia","Agrostemma","Ailanthus","Ajuga","Alcea","Alchemilla","Aletris","Alisma","Allium","Alliaria","Althaea","Alyssum","Amaranthus","Ambrosia","Amelanchier","Amerorchis","Ammophila","Ammannia","Amorpha","Amphicarpaea","Amsinckia","Anagallis","Anaphalis","Arabis","Arnoseris","Arnoglossum","Asplenium","Anchusa","Andropogon","Andromeda","Androsace","Anemone","Anethum","Angelica","Anthemis","Antennaria","Antirrhinum","Anthoxanthum","Anthriscus","Anthyllis","Apera","Apios","Aplectrum","Apocynum","Aquilegia","Aralia","Arabidopsis","Arctium","Arceuthobium","Arctostaphylos","Arethusa","Arenaria","Argemone","Argentina","Aristida","Arisaema","Aristolochia","Armoracia","Aronia","Arrhenatherum","Artemisia","Aruncus","Asarum","Asclepias","Asimina","Asparagus","Astragalus","Aster","Aureolaria","Belamcanda","Athyrium","Atriplex","Avena","Avenula","Azolla","Bacopa","Balsamita","Ballota","Baptisia","Barbarea","Bartonia","Beckmannia","Bellis","Berula","Berteroa","Berberis","Besseya","Betula","Boltonia","Bolboschoenus","Bidens","Blephilia","Boehmeria","Borago","Botrychium","Bromus","Bouteloua","Brachyelytrum","Brachyactis","Brassica","Brasenia","Briza","Buchloe","Buglossoides","Bulbostylis","Bunias","Butomus","Cakile","Callirhoe","Calamintha","Calypso","Calamagrostis","Callistephus","Calystegia","Callitriche","Calamovilfa","Caltha","Calendula","Calopogon","Calla","Calylophus","Capsella","Carduus","Carex","Calluna","Campanula","Camelina","Campsis","Camassia","Cannabis","Caragana","Cardamine","Carpinus","Carum","Carya","Cardaria","Castilleja","Castanea","Catabrosa","Catalpa","Caulophyllum","Cerastium","Ceanothus","Celosia","Celtis","Celastrus","Centaurea","Cenchrus","Centaurium","Cephalaria","Cephalanthus","Cercis","Ceratophyllum","Chenopodium","Cheilanthes","Cirsium","Chamaedaphne","Chamaecrista","Chamaesyce","Chasmanthium","Chaiturus","Chaenorhinum","Chaerophyllum","Chaenomeles","Chelone","Chelidonium","Chimaphila","Chrysosplenium","Chrysanthemum","Cicer","Cicuta","Cichorium","Cimicifuga","Cinna","Circaea","Citrullus","Corallorhiza","Coreopsis","Corispermum","Cornus","Coriandrum","Corydalis","Claytonia","Cladium","Cleome","Clematis","Clintonia","Clinopodium","Cnicus","Coeloglossum","Collinsonia","Collomia","Collinsia","Commelina","Comarum","Comptonia","Comandra","Consolida","Conopholis","Convolvulus","Conyza","Conioselinum","Conium","Convallaria","Conringia","Coptis","Corylus","Coronopus","Crataegus","Coronilla","Cosmos","Cotoneaster","Cucurbita","Cucumis","Crepis","Croton","Crotalaria","Cryptotaenia","Crypsis","Cryptogramma","Cuscuta","Cycloloma","Cymbalaria","Cynoglossum","Cynosurus","Cypripedium","Cyperus","Cystopteris","Dactylis","Dalea","Danthonia","Daphne","Dasistoma","Datura","Daucus","Decodon","Delphinium","Dennstaedtia","Deparia","Desmodium","Deschampsia","Desmanthus","Dicentra","Dichanthelium","Descurainia","Desmazeria","Diarrhena","Dianthus","Digitaria","Digitalis","Diodia","Dioscorea","Didiplis","Diervilla","Draba","Drosera","Dysphania","Diphasiastrum","Dipsacus","Diplotaxis","Diplazium","Dirca","Distichlis","Dodecatheon","Dracocephalum","Dryopteris","Duchesnea","Dulichium","Dyssodia","Echinodorus","Eleocharis","Equisetum","Eragrostis","Echinochloa","Echinocystis","Echinacea","Echinops","Echium","Eclipta","Elaeagnus","Elatine","Eleusine","Ellisia","Elodea","Elsholtzia","Elymus","Elytrigia","Enemion","Epilobium","Epipactis","Epigaea","Epifagus","Erechtites","Erigeron","Eriophorum","Eriocaulon","Erigenia","Eriochloa","Erodium","Erucastrum","Erythronium","Eupatorium","Euphorbia","Euphrasia","Euthamia","Erysimum","Eryngium","Eschscholzia","Euonymus","Filipendula","Fimbristylis","Galium","Galinsoga","Geum","Fagopyrum","Fagus","Falcaria","Fatoua","Festuca","Floerkea","Foeniculum","Fraxinus","Frasera","Fragaria","Froelichia","Fuirena","Fumaria","Gaillardia","Gaillarida","Galeopsis","Galearis","Gaura","Gaultheria","Gaylussacia","Gentiana","Gentianopsis","Gentianella","Genista","Geocaulon","Geranium","Gilia","Grindelia","Helenium","Helianthemum","Glechoma","Gleditsia","Glyceria","Glycyrrhiza","Glycine","Gnaphalium","Goodyera","Gratiola","Guizotia","Gymnocladus","Gymnocarpium","Gypsophila","Hackelia","Halenia","Hamamelis","Hasteola","Hedeoma","Helianthus","Heliopsis","Heterotheca","Heuchera","Hemerocallis","Hepatica","Herniaria","Heracleum","Hesperis","Heteranthera","Hibiscus","Hieracium","Hippuris","Holcus","Holosteum","Hierochloe","Hordeum","Houstonia","Hudsonia","Humulus","Huperzia","Hybanthus","Hydrocotyle","Hydrophyllum","Hydrastis","Hydrilla","Hyoscyamus","Hypericum","Hypoxis","Hypochaeris","Hyssopus","Iberis","Ilex","Impatiens","Inula","Iodanthus","Juncus","Ipomoea","Ipomopsis","Iris","Isoetes","Iva","Jeffersonia","Jovibarba","Juglans","Juniperus","Lechea","Liatris","Justicia","Kalmia","Kalopanax","Kickxia","Knautia","Kochia","Koeleria","Krigia","Kuhnia","Lactuca","Lamium","Laportea","Lapsana","Lappula","Larix","Lathyrus","Ledum","Leersia","Lemna","Leontodon","Leonurus","Lepidium","Leptochloa","Lespedeza","Lesquerella","Leucophysalis","Leucanthemella","Leucanthemum","Levisticum","Leymus","Lysimachia","Lythrum","Matteuccia","Ligustrum","Lilium","Linnaea","Linaria","Lindernia","Linum","Lipocarpha","Liparis","Listera","Lithospermum","Littorella","Lobelia","Lobularia","Lolium","Lonicera","Lotus","Ludwigia","Lupinus","Luzula","Lycopus","Lycopodium","Lycium","Lychnis","Lycopersicon","Lycopodiella","Lygodesmia","Maclura","Madia","Maianthemum","Malva","Malus","Malcolmia","Malaxis","Marrubium","Matricaria","Mazus","Medicago","Medeola","Megalodonta","Mimulus","Mimosa","Mirabilis","Melilotus","Melampyrum","Melica","Mentha","Menispermum","Menyanthes","Mertensia","Microseris","Milium","Miscanthus","Mitella","Mitchella","Molinia","Mollugo","Monarda","Muhlenbergia","Muscari","Monotropa","Moneses","Morus","Myosotis","Myosurus","Myriophyllum","Myrica","Najas","Napaea","Narcissus","Nasturtium","Nelumbo","Nepeta","Neslia","Nicandra","Nicotiana","Nuphar","Oenothera","Nymphaea","Nymphoides","Nyssa","Ocimum","Odontites","Osmunda","Osmorhiza","Oligoneuron","Onopordum","Onosmodium","Onoclea","Onobrychis","Ophioglossum","Opuntia","Origanum","Ornithogalum","Orobanche","Orthilia","Oryzopsis","Ostrya","Oxalis","Oxytropis","Oxypolis","Packera","Panax","Panicum","Papaver","Paronychia","Paspalum","Pachysandra","Parnassia","Parthenium","Parietaria","Parthenocissus","Pastinaca","Pediomelum","Pedicularis","Pellaea","Phegopteris","Peltandra","Penstemon","Pentaphylloides","Pennisetum","Penthorum","Perilla","Petunia","Petasites","Petrorhagia","Phalaris","Phacelia","Phellodendron","Phemeranthus","Philadelphus","Phyllanthus","Physostegia","Physalis","Polygonum","Phlox","Phleum","Phoradendron","Phragmites","Phryma","Phytolacca","Phyla","Physocarpus","Picea","Pilea","Pimpinella","Pinus","Pinguicula","Platanthera","Plantago","Plagiobothrys","Platanus","Pluchea","Poa","Podophyllum","Pogonia","Polystichum","Polygonella","Polygonatum","Polemonium","Polymnia","Polygala","Polanisia","Polypogon","Polytaenia","Polypodium","Populus","Pterospora","Pteridium","Pontederia","Portulaca","Potamogeton","Potentilla","Prenanthes","Primula","Proserpinaca","Prunus","Prunella","Psoralidium","Ptelea","Puccinellia","Pulmonaria","Pycnanthemum","Pyrola","Ranunculus","Pyrus","Quercus","Raphanus","Rapistrum","Ratibida","Reseda","Rhamnus","Rheum","Rhexia","Rhinanthus","Rhododendron","Rhodotypos","Rhus","Rhynchospora","Ribes","Robinia","Rorippa","Rosa","Rotala","Rubus","Rudbeckia","Ruellia","Rumex","Ruppia","Ruta","Sabatia","Sagittaria","Salix","Sagina","Salvia","Salsola","Salicornia","Sanicula","Sanguisorba","Saponaria","Sarracenia","Sassafras","Sambucus","Samolus","Sanguinaria","Satureja","Saururus","Saxifraga","Scleranthus","Sesamum","Setaria","Schoenoplectus","Scheuchzeria","Schedonnardus","Schizachne","Schizachyrium","Scirpus","Scilla","Scleria","Scrophularia","Scutellaria","Secale","Sedum","Selaginella","Senecio","Senna","Shepherdia","Sherardia","Sibbaldiopsis","Sicyos","Silene","Silphium","Sinapis","Sisyrinchium","Sisymbrium","Solidago","Solanum","Spergularia","Sium","Smilax","Sonchus","Sorbus","Sorghum","Sorghastrum","Sorbaria","Sparganium","Spartina","Spergula","Sphenopholis","Spiraea","Spiranthes","Sporobolus","Spirodela","Streptopus","Strophostyles","Stuckenia","Thalictrum","Stachys","Staphylea","Stellaria","Stipa","Stylosanthes","Stylophorum","Suaeda","Sullivantia","Symphoricarpos","Symphytum","Symplocarpus","Syringa","Taenidia","Tagetes","Tanacetum","Taraxacum","Taxus","Tephrosia","Tetragonia","Teucrium","Thaspium","Thelypteris","Thermopsis","Thlaspi","Thuja","Thymelaea","Thymus","Tiarella","Tilia","Tomanthera","Torilis","Toxicodendron","Tradescantia","Tragopogon","Triticum","Trichophorum","Trifolium","Triosteum","Trientalis","Trichostema","Trillium","Tridens","Triadenum","Triantha","Tripleurospermum","Triplasis","Triglochin","Trisetum","Triodanis","Tribulus","Triphora","Vaccinium","Vallisneria","Tsuga","Tussilago","Typha","Ulmus","Urtica","Utricularia","Uvularia","Vaccaria","Valerianella","Valeriana","Ventenata","Verbesina","Veronica","Vernonia","Verbena","Verbascum","Veronicastrum","Viburnum","Vicia","Viola","Vitis","Vinca","Vincetoxicum","Zigadenus","Zizia","Zizania","Vulpia","Waldsteinia","Wolffia","Wolffiella","Woodsia","Xanthium","Xyris","Yucca","Zanthoxylum","Zannichellia","Zea"]

class CountHandler(webapp2.RequestHandler):
    """CountHandler homepage viewer
    """
    #logging.info('CountHandler was called')
    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('count.html')
        #qSpecimen = models.Specimen.all()
        #qSpecies = models.Species.all()
        queryResults = models.Specimen.all()
        #queryResults = queryResults.fetch(100, offset=96800).fetch(20)
        #queryResults = queryResults.fetch(100, offset=96800)
        offsetSkip=349900
        queryNumber = queryResults.count(1, offset=offsetSkip)
        values = dict()
        values['xtrahtml'] = '----------------------COUNT--------------------------<br>'
        #for specimenEntity in queryResults:
            #values['xtrahtml'] += 'ACCESSION %s<br>' % (specimenEntity.ACCESSION)
        values['xtrahtml'] += 'Count for offset: %d %d' % (queryNumber, offsetSkip)
        values['xtrahtml'] += '----------------------------------------------------<br>'
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'xtrahtml': values['xtrahtml']
        }
        self.response.out.write(template.render(context))

class GenusViewHandler(webapp2.RequestHandler):
    """GenusViewHandler homepage viewer
    """
    #logging.info('GenusViewHandler was called')
    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('view.html')
        genus = self.request.get('genus')
        q = models.Species.all().filter('genus =', genus)
        values = dict()
        values['xtrahtml'] = '----------------------view %s-----------------------<br>' % (genus)
        for speciesEntity in q:
            values['xtrahtml'] += '<h2>Family: %s</h2>' % (speciesEntity.FAMILY)
            values['xtrahtml'] += '<h3>Genus: %s</h3>' % (speciesEntity.genus)
            values['xtrahtml'] += '%s' % (speciesEntity.Taxa)
            if (speciesEntity.Photo is not None):
                values['xtrahtml'] += '*'
            if (speciesEntity.Thumbmaps is not None):
                values['xtrahtml'] += '+'
            values['xtrahtml'] += '<br><a href="/specimenlist?taxcd=%s">Get Specimens for Taxcd %s</a><br>' % (speciesEntity.Taxcd, speciesEntity.Taxcd)

        values['xtrahtml'] += '----------------------------------------------------<br>'
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'xtrahtml': values['xtrahtml']
        }
        self.response.out.write(template.render(context))

class FamilyViewHandler(webapp2.RequestHandler):
    """FamilyViewHandler homepage viewer
    """
    #logging.info('FamilyViewHandler was called')
    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('view.html')
        family = self.request.get('family')
        #q = models.Species.all().filter('FAMILY =', family)
        q = models.Species.all().filter('FAMILY =', family).filter('Syncd =', '.')
        values = dict()
        values['xtrahtml'] = '----------------------view--------------------------<br>'
        for speciesEntity in q:
            values['xtrahtml'] += '<h2>Family: %s</h2>' % (speciesEntity.FAMILY)
            values['xtrahtml'] += '<h3>Genus: %s</h3>' % (speciesEntity.genus)
            values['xtrahtml'] += '%s' % (speciesEntity.Taxa)
            if (speciesEntity.Photo is not None):
                values['xtrahtml'] += '*'
            if (speciesEntity.Thumbmaps is not None):
                values['xtrahtml'] += '+'
            values['xtrahtml'] += '<br><a href="/specimenlist?taxcd=%s">Get Specimens for Taxcd %s</a><br>' % (speciesEntity.Taxcd, speciesEntity.Taxcd)

        values['xtrahtml'] += '----------------------------------------------------<br>'
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'xtrahtml': values['xtrahtml']
        }
        self.response.out.write(template.render(context))

class SpecimenListViewHandler(webapp2.RequestHandler):
    """SpecimenListViewHandler homepage viewer
    """
    #logging.info('SpecimenListViewHandler was called')
    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('view.html')
        taxcd = self.request.get('taxcd')
        q = models.Specimen.all().filter('TAXCD =', taxcd)
        values = dict()
        values['xtrahtml'] = '----------------View Specimens For %s ----------------<br>' % (taxcd)
        values['xtrahtml'] += '<table><tr><td>Accession</td><td>Taxon</td><td>Date</td><td>Collector</td><td>Coll No.</td><td>County</td><tr>'
        for specimenEntity in q:
            values['xtrahtml'] += '<tr>'
            values['xtrahtml'] += '<td><a href="/specimen?accession=%s">%s</a></td>' % (specimenEntity.ACCESSION, specimenEntity.ACCESSION)
            values['xtrahtml'] += '<td>%s</td>' % (specimenEntity.TAXCD)
            values['xtrahtml'] += '<td>%s</td>' % (specimenEntity.COLLDATE)
            values['xtrahtml'] += '<td>%s</td>' % (specimenEntity.COLL1NAME)
            values['xtrahtml'] += '<td>%s</td>' % (specimenEntity.COLLNO1)
            values['xtrahtml'] += '<td>%s</td>' % (specimenEntity.COUNTY)
            values['xtrahtml'] += '</tr>'

        values['xtrahtml'] += '</table>'
        values['xtrahtml'] += '----------------------------------------------------<br>'
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'xtrahtml': values['xtrahtml']
        }
        self.response.out.write(template.render(context))

#SpecimenViewHandler
class SpecimenViewHandler(webapp2.RequestHandler):
    """SpecimenViewHandler homepage viewer
    """
    #logging.info('SpecimenViewHandler was called')
    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('view.html')
        accession = self.request.get('accession')
        q = models.Specimen.all().filter('ACCESSION =', accession)
        values = dict()
        values['xtrahtml'] = '----------------------view %s----------------------<br>' % (accession)
        for specimenEntity in q:
            #values['xtrahtml'] += 'Specimen Accession %s</a><br>' % (specimenEntity.ACCESSION)
            #values['xtrahtml'] += 'Specimen Collector %s</a><br>' % (specimenEntity.COLL1NAME)
            #This code should work-see book pgae2 pg 145 near "instance_properties()"
            #for propertyName in specimenEntity.instance_properties(): 
                #propertyValue = getattr(specimenEntity, propertyName)
                #values['xtrahtml'] += '<b>%s<b>: %s<br>' % (propertyName, propertyValue)
            values['xtrahtml'] += '<br>ACCESSION: %s' % (specimenEntity.ACCESSION)
            values['xtrahtml'] += '<br>TYPE: %s' % (specimenEntity.TYPE)
            values['xtrahtml'] += '<br>COLLDATE: %s' % (specimenEntity.COLLDATE)
            values['xtrahtml'] += '<br>FLOWER: %s' % (specimenEntity.FLOWER)
            values['xtrahtml'] += '<br>FRUIT: %s' % (specimenEntity.FRUIT)
            values['xtrahtml'] += '<br>STERILE: %s' % (specimenEntity.STERILE)
            values['xtrahtml'] += '<br>OBJTYPE: %s' % (specimenEntity.OBJTYPE)
            values['xtrahtml'] += '<br>INST: %s' % (specimenEntity.INST)
            values['xtrahtml'] += '<br>ANNCODE: %s' % (specimenEntity.ANNCODE)
            values['xtrahtml'] += '<br>ANNDATE: %s' % (specimenEntity.ANNDATE)
            values['xtrahtml'] += '<br>ANNSOURCE: %s' % (specimenEntity.ANNSOURCE)
            values['xtrahtml'] += '<br>CITY: %s' % (specimenEntity.CITY)
            values['xtrahtml'] += '<br>SITENO: %s' % (specimenEntity.SITENO)
            values['xtrahtml'] += '<br>CITYTYPE: %s' % (specimenEntity.CITYTYPE)
            values['xtrahtml'] += '<br>COLL2NAME: %s' % (specimenEntity.COLL2NAME)
            values['xtrahtml'] += '<br>COLL3NAME: %s' % (specimenEntity.COLL3NAME)
            values['xtrahtml'] += '<br>COLL1NAME: %s' % (specimenEntity.COLL1NAME)
            values['xtrahtml'] += '<br>COLLNO1: %s' % (specimenEntity.COLLNO1)
            values['xtrahtml'] += '<br>COLLEVENT: %s' % (specimenEntity.COLLEVENT)
            values['xtrahtml'] += '<br>TAXCD: %s' % (specimenEntity.TAXCD)
            values['xtrahtml'] += '<br>CFS: %s' % (specimenEntity.CFS)
            values['xtrahtml'] += '<br>CFV: %s' % (specimenEntity.CFV)
            values['xtrahtml'] += '<br>CFVariety: %s' % (specimenEntity.CFVariety)
            values['xtrahtml'] += '<br>HABITAT_MISC: %s' % (specimenEntity.HABITAT_MISC)
            values['xtrahtml'] += '<br>HABITAT: %s' % (specimenEntity.HABITAT)
            values['xtrahtml'] += '<br>LONGX: %s' % (specimenEntity.LONGX)
            values['xtrahtml'] += '<br>LAT: %s' % (specimenEntity.LAT)
            values['xtrahtml'] += '<br>ELEV: %s' % (specimenEntity.ELEV)
            values['xtrahtml'] += '<br>LLGENER: %s' % (specimenEntity.LLGENER)
            values['xtrahtml'] += '<br>LONG2: %s' % (specimenEntity.LONG2)
            values['xtrahtml'] += '<br>LAT2: %s' % (specimenEntity.LAT2)
            values['xtrahtml'] += '<br>LTDEC: %s' % (specimenEntity.LTDEC)
            values['xtrahtml'] += '<br>LGDEC: %s' % (specimenEntity.LGDEC)
            values['xtrahtml'] += '<br>NOWLOC: %s' % (specimenEntity.NOWLOC)
            values['xtrahtml'] += '<br>LOAN: %s' % (specimenEntity.LOAN)
            values['xtrahtml'] += '<br>PAGES: %s' % (specimenEntity.PAGES)
            values['xtrahtml'] += '<br>ORIGCD: %s' % (specimenEntity.ORIGCD)
            values['xtrahtml'] += '<br>PUBCD: %s' % (specimenEntity.PUBCD)
            values['xtrahtml'] += '<br>LITCIT: %s' % (specimenEntity.LITCIT)
            values['xtrahtml'] += '<br>PUBDATE: %s' % (specimenEntity.PUBDATE)
            values['xtrahtml'] += '<br>PUBDATEA: %s' % (specimenEntity.PUBDATEA)
            values['xtrahtml'] += '<br>VERPERS: %s' % (specimenEntity.VERPERS)
            values['xtrahtml'] += '<br>VERDATE: %s' % (specimenEntity.VERDATE)
            values['xtrahtml'] += '<br>EX: %s' % (specimenEntity.EX)
            values['xtrahtml'] += '<br>ARTICLE: %s' % (specimenEntity.ARTICLE)
            values['xtrahtml'] += '<br>PREC: %s' % (specimenEntity.PREC)
            values['xtrahtml'] += '<br>STATEL: %s' % (specimenEntity.STATEL)
            values['xtrahtml'] += '<br>COUNTY: %s' % (specimenEntity.COUNTY)
            values['xtrahtml'] += '<br>COUNTRY: %s' % (specimenEntity.COUNTRY)
            values['xtrahtml'] += '<br>T1: %s' % (specimenEntity.T1)
            values['xtrahtml'] += '<br>R1: %s' % (specimenEntity.R1)
            values['xtrahtml'] += '<br>S1: %s' % (specimenEntity.S1)
            values['xtrahtml'] += '<br>NSEW_1: %s' % (specimenEntity.NSEW_1)
            values['xtrahtml'] += '<br>TRSGENER: %s' % (specimenEntity.TRSGENER)
            values['xtrahtml'] += '<br>T2: %s' % (specimenEntity.T2)
            values['xtrahtml'] += '<br>R2: %s' % (specimenEntity.R2)
            values['xtrahtml'] += '<br>S2: %s' % (specimenEntity.S2)
            values['xtrahtml'] += '<br>NSEW_2: %s' % (specimenEntity.NSEW_2)
            values['xtrahtml'] += '<br>PLACE: %s' % (specimenEntity.PLACE)
            values['xtrahtml'] += '<br>scan: %s' % (specimenEntity.scan)
            values['xtrahtml'] += '<br>MAPFILE: %s' % (specimenEntity.MAPFILE)
            values['xtrahtml'] += '<br>username: %s' % (specimenEntity.username)
            values['xtrahtml'] += '<br>date_time: %s' % (specimenEntity.date_time)
            values['xtrahtml'] += '<br>DTRS: %s' % (specimenEntity.DTRS)
            values['xtrahtml'] += '<br>PKID: %s' % (specimenEntity.PKID)
        values['xtrahtml'] += '----------------------------------------------------<br>'
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'xtrahtml': values['xtrahtml']
        }
        self.response.out.write(template.render(context))


class ViewHandler(webapp2.RequestHandler):
    """ViewHandler homepage viewer
    """
    #logging.info('ViewHandler was called')
    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('view.html')
        q = models.Species.all()
        queryResults = q.fetch(10)
        values = dict()
        values['xtrahtml'] = '----------------------view--------------------------<br>'
        for speciesEntity in queryResults:
            values['xtrahtml'] += 'Taxcd %s<br>' % (speciesEntity.Taxcd)

        values['xtrahtml'] += '----------------------------------------------------<br>'
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'xtrahtml': values['xtrahtml']
        }
        self.response.out.write(template.render(context))

class ViewSpecimensViaSpeciesHandler(webapp2.RequestHandler):
    """ViewSpecimensViaSpeciesHandler homepage viewer
    """
    #logging.info('ViewSpecimensViaSpeciesHandler was called')
    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('view.html')
        q = models.Species.all().filter("Taxcd =", "ABIBAL")
        #q = models.Species.all()
        queryResults = q.fetch(3)
        values = dict()
        values['xtrahtml'] = '----------------------view spec via spd--------------<br>'
        for speciesEntity in queryResults:
            values['xtrahtml'] += 'Taxcd %s<br>' % (speciesEntity.Taxcd)
            for specimenEntity in speciesEntity.specimen_set:
                    values['xtrahtml'] += 'Accession %s<br>' % (specimenEntity.ACCESSION)

        values['xtrahtml'] += '----------------------------------------------------<br>'
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'xtrahtml': values['xtrahtml']
        }
        self.response.out.write(template.render(context))
       

       


class MainHandler(webapp2.RequestHandler):
    """MainHandler homepage viewer
    """
    #logging.info('MainHandler was called')
    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('addspecies.html')
        values = dict()
        if user:
            values['xtrahtml'] = '----------------------------------------------------'
            values['xtrahtml'] += '<br><a href="/families">Families</a><br>'
            values['xtrahtml'] += '<br><a href="/genera">Genera</a><br>'
            values['xtrahtml'] += '----------------------------------------------------'
        else:
            values['xtrahtml'] = '----------------------------------------------------'
            values['xtrahtml'] = 'Login is required'
            values['xtrahtml'] = '----------------------------------------------------'

        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'xtrahtml': values['xtrahtml']
        }
        self.response.out.write(template.render(context))

class FamilyHandler(webapp2.RequestHandler):
    """FamilyHandler homepage viewer
    """
    #logging.info('FamilyHandler was called')
    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('addspecies.html')
        values = dict()
        values['xtrahtml'] = '----------------------------------------------------'
        for family in familyList:
            values['xtrahtml'] += '<a href="/family?family=%s">%s</a><br>' % (family,family)
        values['xtrahtml'] += '----------------------------------------------------'
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'xtrahtml': values['xtrahtml']
        }
        self.response.out.write(template.render(context))

class GenusHandler(webapp2.RequestHandler):
    """GenusHandler homepage viewer
    """
    #logging.info('GenusHandler was called')
    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        template = template_env.get_template('addspecies.html')
        values = dict()
        values['xtrahtml'] = '----------------------------------------------------'
        for genus in genusList:
            values['xtrahtml'] += '<a href="/genus?genus=%s">%s</a><br>' % (genus,genus)
        values['xtrahtml'] += '----------------------------------------------------'
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'xtrahtml': values['xtrahtml']
        }
        self.response.out.write(template.render(context))


class AddSpecimenHandler(webapp2.RequestHandler):
    """AddSpecimenHandler adds specimen records to the datastore
    """
    #logging.info('AddSpecimenHandler was called')

    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        addspecimenhtml = """
        <form action="/addspecimen" method="POST">
        ACCESSION <input type="text" name="ACCESSION" value="ACCESSION"><br>
        TYPE <input type="text" name="TYPE" value="TYPE"><br>
        COLLDATE <input type="text" name="COLLDATE" value="COLLDATE"><br>
        FLOWER <input type="text" name="FLOWER" value="FLOWER"><br>
        FRUIT <input type="text" name="FRUIT" value="FRUIT"><br>
        STERILE <input type="text" name="STERILE" value="STERILE"><br>
        OBJTYPE <input type="text" name="OBJTYPE" value="OBJTYPE"><br>
        INST <input type="text" name="INST" value="INST"><br>
        ANNCODE <input type="text" name="ANNCODE" value="ANNCODE"><br>
        ANNDATE <input type="text" name="ANNDATE" value="ANNDATE"><br>
        ANNSOURCE <input type="text" name="ANNSOURCE" value="ANNSOURCE"><br>
        CITY <input type="text" name="CITY" value="CITY"><br>
        SITENO <input type="text" name="SITENO" value="SITENO"><br>
        CITYTYPE <input type="text" name="CITYTYPE" value="CITYTYPE"><br>
        COLL2NAME <input type="text" name="COLL2NAME" value="COLL2NAME"><br>
        COLL3NAME <input type="text" name="COLL3NAME" value="COLL3NAME"><br>
        COLL1NAME <input type="text" name="COLL1NAME" value="COLL1NAME"><br>
        COLLNO1 <input type="text" name="COLLNO1" value="COLLNO1"><br>
        COLLEVENT <input type="text" name="COLLEVENT" value="COLLEVENT"><br>
        TAXCD <input type="text" name="TAXCD" value="TAXCD"><br>
        CFS <input type="text" name="CFS" value="CFS"><br>
        CFV <input type="text" name="CFV" value="CFV"><br>
        CFVariety <input type="text" name="CFVariety" value="CFVariety"><br>
        HABITAT_MISC <input type="text" name="HABITAT_MISC" value="HABITAT_MISC"><br>
        HABITAT <input type="text" name="HABITAT" value="HABITAT"><br>
        LONGX <input type="text" name="LONGX" value="LONGX"><br>
        LAT <input type="text" name="LAT" value="LAT"><br>
        ELEV <input type="text" name="ELEV" value="ELEV"><br>
        LLGENER <input type="text" name="LLGENER" value="LLGENER"><br>
        LONG2 <input type="text" name="LONG2" value="LONG2"><br>
        LAT2 <input type="text" name="LAT2" value="LAT2"><br>
        LTDEC <input type="text" name="LTDEC" value="LTDEC"><br>
        LGDEC <input type="text" name="LGDEC" value="LGDEC"><br>
        NOWLOC <input type="text" name="NOWLOC" value="NOWLOC"><br>
        LOAN <input type="text" name="LOAN" value="LOAN"><br>
        PAGES <input type="text" name="PAGES" value="PAGES"><br>
        ORIGCD <input type="text" name="ORIGCD" value="ORIGCD"><br>
        PUBCD <input type="text" name="PUBCD" value="PUBCD"><br>
        LITCIT <input type="text" name="LITCIT" value="LITCIT"><br>
        PUBDATE <input type="text" name="PUBDATE" value="PUBDATE"><br>
        PUBDATEA <input type="text" name="PUBDATEA" value="PUBDATEA"><br>
        VERPERS <input type="text" name="VERPERS" value="VERPERS"><br>
        VERDATE <input type="text" name="VERDATE" value="VERDATE"><br>
        EX <input type="text" name="EX" value="EX"><br>
        ARTICLE <input type="text" name="ARTICLE" value="ARTICLE"><br>
        PREC <input type="text" name="PREC" value="PREC"><br>
        STATEL <input type="text" name="STATEL" value="STATEL"><br>
        COUNTY <input type="text" name="COUNTY" value="COUNTY"><br>
        COUNTRY <input type="text" name="COUNTRY" value="COUNTRY"><br>
        T1 <input type="text" name="T1" value="T1"><br>
        R1 <input type="text" name="R1" value="R1"><br>
        S1 <input type="text" name="S1" value="S1"><br>
        NSEW_1 <input type="text" name="NSEW_1" value="NSEW_1"><br>
        TRSGENER <input type="text" name="TRSGENER" value="TRSGENER"><br>
        T2 <input type="text" name="T2" value="T2"><br>
        R2 <input type="text" name="R2" value="R2"><br>
        S2 <input type="text" name="S2" value="S2"><br>
        NSEW_2 <input type="text" name="NSEW_2" value="NSEW_2"><br>
        PLACE <input type="text" name="PLACE" value="PLACE"><br>
        scan <input type="text" name="scan" value="scan"><br>
        MAPFILE <input type="text" name="MAPFILE" value="MAPFILE"><br>
        username <input type="text" name="username" value="username"><br>
        date_time <input type="text" name="date_time" value="date_time"><br>
        PKID <input type="text" name="PKID" value="PKID"><br>
        DTRS <input type="text" name="DTRS" value="DTRS"><br>

        <input type="submit" value="Add Specimen Record"><br>
        </form>
        """
        values = dict()
        values['xtrahtml'] = addspecimenhtml

        template = template_env.get_template('addspecimen.html')
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'xtrahtml': values['xtrahtml']
        }
        self.response.out.write(template.render(context))

    def post(self):
        #Find the TAXCD of the ASN for the Specimen being posted
        # Specimen.TAXCD should have a value of Species.Taxcd for when Species.Syn='.'
        speciesTaxcdASN = self.request.get('TAXCD')
        queryResults = models.Species.all().filter("Taxcd =", speciesTaxcdASN)
        #species should have one Species entity..or Python None if zero results:
        species = queryResults.get()
        specimenInstance = models.Specimen(ACCESSION = self.request.get('ACCESSION'),
        TYPE = self.request.get('TYPE'),
        COLLDATE = self.request.get('COLLDATE'),
        FLOWER = self.request.get('FLOWER'),
        FRUIT = self.request.get('FRUIT'),
        STERILE = self.request.get('STERILE'),
        OBJTYPE = self.request.get('OBJTYPE'),
        INST = self.request.get('INST'),
        ANNCODE = self.request.get('ANNCODE'),
        ANNDATE = self.request.get('ANNDATE'),
        ANNSOURCE = self.request.get('ANNSOURCE'),
        CITY = self.request.get('CITY'),
        SITENO = self.request.get('SITENO'),
        CITYTYPE = self.request.get('CITYTYPE'),
        COLL2NAME = self.request.get('COLL2NAME'),
        COLL3NAME = self.request.get('COLL3NAME'),
        COLL1NAME = self.request.get('COLL1NAME'),
        COLLNO1 = self.request.get('COLLNO1'),
        COLLEVENT = self.request.get('COLLEVENT'),
        TAXCD = self.request.get('TAXCD'),
        CFS = self.request.get('CFS'),
        CFV = self.request.get('CFV'),
        CFVariety = self.request.get('CFVariety'),
        HABITAT_MISC = self.request.get('HABITAT_MISC'),
        HABITAT = self.request.get('HABITAT'),
        LONGX = self.request.get('LONGX'),
        LAT = self.request.get('LAT'),
        ELEV = self.request.get('ELEV'),
        LLGENER = self.request.get('LLGENER'),
        LONG2 = self.request.get('LONG2'),
        LAT2 = self.request.get('LAT2'),
        LTDEC = self.request.get('LTDEC'),
        LGDEC = self.request.get('LGDEC'),
        NOWLOC = self.request.get('NOWLOC'),
        LOAN = self.request.get('LOAN'),
        PAGES = self.request.get('PAGES'),
        ORIGCD = self.request.get('ORIGCD'),
        PUBCD = self.request.get('PUBCD'),
        LITCIT = self.request.get('LITCIT'),
        PUBDATE = self.request.get('PUBDATE'),
        PUBDATEA = self.request.get('PUBDATEA'),
        VERPERS = self.request.get('VERPERS'),
        VERDATE = self.request.get('VERDATE'),
        EX = self.request.get('EX'),
        ARTICLE = self.request.get('ARTICLE'),
        PREC = self.request.get('PREC'),
        STATEL = self.request.get('STATEL'),
        COUNTY = self.request.get('COUNTY'),
        COUNTRY = self.request.get('COUNTRY'),
        T1 = self.request.get('T1'),
        R1 = self.request.get('R1'),
        S1 = self.request.get('S1'),
        NSEW_1 = self.request.get('NSEW_1'),
        TRSGENER = self.request.get('TRSGENER'),
        T2 = self.request.get('T2'),
        R2 = self.request.get('R2'),
        S2 = self.request.get('S2'),
        NSEW_2 = self.request.get('NSEW_2'),
        PLACE = self.request.get('PLACE'),
        scan = self.request.get('scan'),
        MAPFILE = self.request.get('MAPFILE'),
        username = self.request.get('username'),
        date_time = self.request.get('date_time'),
        PKID = self.request.get('PKID'),
        DTRS = self.request.get('DTRS'),
        species = species)

        #logging.info('about to put a Specimen')
        specimenInstance.put()

        #logging.info('posted to addspecimen')
        self.get()

        self.redirect('/')



class AddSpeciesHandler(webapp2.RequestHandler):
    """AddSpeciesHandler adds species records to the datastore
    """
    #logging.info('AddSpeciesHandler was called')

    def get(self):

        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)

        addspecieshtml = """
        <form action="/addspecies" method="POST">
        Taxcd  <input type="text" name="Taxcd" value="Taxcd"><br>
        Syncd  <input type="text" name="Syncd" value="Syncd"><br>
        family_code  <input type="text" name="family_code" value="family_code"><br>
        genus  <input type="text" name="genus" value="genus"><br>
        species  <input type="text" name="species" value="species"><br>
        authority  <input type="text" name="authority" value="authority"><br>
        subsp  <input type="text" name="subsp" value="subsp"><br>
        variety  <input type="text" name="variety" value="variety"><br>
        forma  <input type="text" name="forma" value="forma"><br>
        subsp_auth  <input type="text" name="subsp_auth" value="subsp_auth"><br>
        var_auth  <input type="text" name="var_auth" value="var_auth"><br>
        forma_auth  <input type="text" name="forma_auth" value="forma_auth"><br>
        sub_family  <input type="text" name="sub_family" value="sub_family"><br>
        tribe  <input type="text" name="tribe" value="tribe"><br>
        common  <input type="text" name="common" value="common"><br>
        Wisc_found  <input type="text" name="Wisc_found" value="Wisc_found"><br>
        ssp  <input type="text" name="ssp" value="ssp"><br>
        var  <input type="text" name="var" value="var"><br>
        f  <input type="text" name="f" value="f"><br>
        hybrids  <input type="text" name="hybrids" value="hybrids"><br>
        status_code  <input type="text" name="status_code" value="status_code"><br>
        hide  <input type="text" name="hide" value="hide"><br>
        USDA  <input type="text" name="USDA" value="USDA"><br>
        COFC  <input type="text" name="COFC" value="COFC"><br>
        WETINDICAT  <input type="text" name="WETINDICAT" value="WETINDICAT"><br>
        FAM_NAME  <input type="text" name="FAM_NAME" value="FAM_NAME"><br>
        FAMILY  <input type="text" name="FAMILY" value="FAMILY"><br>
        GC  <input type="text" name="GC" value="GC"><br>
        FAMILY_COMMON  <input type="text" name="FAMILY_COMMON" value="FAMILY_COMMON"><br>
        SYNWisc_found  <input type="text" name="SYNWisc_found" value="SYNWisc_found"><br>
        SYNS_STATUS  <input type="text" name="SYNS_STATUS" value="SYNS_STATUS"><br>
        SYNV_STATUS  <input type="text" name="SYNV_STATUS" value="SYNV_STATUS"><br>
        SYNF_STATUS  <input type="text" name="SYNF_STATUS" value="SYNF_STATUS"><br>
        SYNHYBRIDS_STATUS  <input type="text" name="SYNHYBRIDS_STATUS" value="SYNHYBRIDS_STATUS"><br>
        SYNW_STATUS  <input type="text" name="SYNW_STATUS" value="SYNW_STATUS"><br>
        speciesweb_Taxcd  <input type="text" name="speciesweb_Taxcd" value="speciesweb_Taxcd"><br>
        Status  <input type="text" name="Status" value="Status"><br>
        Photo  <input type="text" name="Photo" value="Photo"><br>
        Photographer  <input type="text" name="Photographer" value="Photographer"><br>
        Thumbmaps  <input type="text" name="Thumbmaps" value="Thumbmaps"><br>
        Accgenus  <input type="text" name="Accgenus" value="Accgenus"><br>
        SORTOR  <input type="text" name="SORTOR" value="SORTOR"><br>
        Hand  <input type="text" name="Hand" value="Hand"><br>
        growth_habit_bck  <input type="text" name="growth_habit_bck" value="growth_habit_bck"><br>
        blooming_dt_bck  <input type="text" name="blooming_dt_bck" value="blooming_dt_bck"><br>
        origin_bck  <input type="text" name="origin_bck" value="origin_bck"><br>
        Thumbphoto  <input type="text" name="Thumbphoto" value="Thumbphoto"><br>
        date_time  <input type="text" name="date_time" value="date_time"><br>
        growth_habit  <input type="text" name="growth_habit" value="growth_habit"><br>
        blooming_dt  <input type="text" name="blooming_dt" value="blooming_dt"><br>
        origin  <input type="text" name="origin" value="origin"><br>
        Taxa  <input type="text" name="Taxa" value="Taxa"><br>
        <input type="submit" value="Add Species Record"><br>
        </form>
        """
        values = dict()
        values['xtrahtml'] = addspecieshtml

        template = template_env.get_template('addspecies.html')
        context = {
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'xtrahtml': values['xtrahtml']
        }
        self.response.out.write(template.render(context))



    def post(self):
        #Get the Specimen entities from the DS for this species, as a list
        # Later on, we'll add this to the Species.specimen property, a ListProperty(db.Key())
        queryRelatedSpecimens = models.Specimen.all().filter("TAXCD =", self.request.get('Taxcd'))
        #k = db.Key.from_path('Entity',
        #relatedSpecimensKeyList = ['agpkZXZ-aGVyYjE4cg0LEgdTcGVjaWVzGAEM']
        #relatedSpecimensKeyList = [db.Key.from_path('Specimen','agpkZXZ-aGVyYjE4cg0LEgdTcGVjaWVzGAEM')]
        #relatedSpecimensKeyList = []
        relatedSpecimensKeyList = [db.Key.from_path('Specimen','agpkZXZ-aGVyYjE4cg0LEgdTcGVjaWVzGAEM')]
        for specimenEntity in queryRelatedSpecimens:
            relatedSpecimensKeyList.append(specimenEntity.key()) 

        speciesInstance = models.Species(Taxcd = self.request.get('Taxcd'),
        Syncd = self.request.get('Syncd'),
        family_code = self.request.get('family_code'),
        genus = self.request.get('genus'),
        species = self.request.get('species'),
        authority = self.request.get('authority'),
        subsp = self.request.get('subsp'),
        variety = self.request.get('variety'),
        forma = self.request.get('forma'),
        subsp_auth = self.request.get('subsp_auth'),
        var_auth = self.request.get('var_auth'),
        forma_auth = self.request.get('forma_auth'),
        sub_family = self.request.get('sub_family'),
        tribe = self.request.get('tribe'),
        common = self.request.get('common'),
        Wisc_found = self.request.get('Wisc_found'),
        ssp = self.request.get('ssp'),
        var = self.request.get('var'),
        f = self.request.get('f'),
        hybrids = self.request.get('hybrids'),
        status_code = self.request.get('status_code'),
        hide = self.request.get('hide'),
        USDA = self.request.get('USDA'),
        COFC = self.request.get('COFC'),
        WETINDICAT = self.request.get('WETINDICAT'),
        FAM_NAME = self.request.get('FAM_NAME'),
        FAMILY = self.request.get('FAMILY'),
        GC = self.request.get('GC'),
        FAMILY_COMMON = self.request.get('FAMILY_COMMON'),
        SYNWisc_found = self.request.get('SYNWisc_found'),
        SYNS_STATUS = self.request.get('SYNS_STATUS'),
        SYNV_STATUS = self.request.get('SYNV_STATUS'),
        SYNF_STATUS = self.request.get('SYNF_STATUS'),
        SYNHYBRIDS_STATUS = self.request.get('SYNHYBRIDS_STATUS'),
        SYNW_STATUS = self.request.get('SYNW_STATUS'),
        speciesweb_Taxcd = self.request.get('speciesweb_Taxcd'),
        Status = self.request.get('Status'),
        Photo = self.request.get('Photo'),
        Photographer = self.request.get('Photographer'),
        Thumbmaps = self.request.get('Thumbmaps'),
        Accgenus = self.request.get('Accgenus'),
        SORTOR = self.request.get('SORTOR'),
        Hand = self.request.get('Hand'),
        growth_habit_bck = self.request.get('growth_habit_bck'),
        blooming_dt_bck = self.request.get('blooming_dt_bck'),
        origin_bck = self.request.get('origin_bck'),
        Thumbphoto = self.request.get('Thumbphoto'),
        date_time = self.request.get('date_time'),
        growth_habit = self.request.get('growth_habit'),
        blooming_dt = self.request.get('blooming_dt'),
        origin = self.request.get('origin'),
        Taxa = self.request.get('Taxa'),
        #PKID = self.request.get('PKID'))
        #specimens = queryRelatedSpecimens.fetch(990))
        specimens = relatedSpecimensKeyList)
        speciesInstance.put()

        #logging.info('posted to addspecies')
        self.get()

        self.redirect('/')


application = webapp2.WSGIApplication(
    [('/', MainHandler),
     ('/addspecies', AddSpeciesHandler),
     ('/addspecimen', AddSpecimenHandler),
     ('/count', CountHandler),
     #('/countspecs', CountSpecimensInSpeciesHandler),
     #('/getspecimenfromspecies', GetSpecimenFromSpeciesHandler),
     ('/families', FamilyHandler),
     ('/genera', GenusHandler),
     ('/family?.*', FamilyViewHandler),
     ('/genus?.*', GenusViewHandler),
     ('/specimenlist.*', SpecimenListViewHandler),
     ('/specimen.*', SpecimenViewHandler),
     ('/getspecimenfromspecies', ViewSpecimensViaSpeciesHandler),
     ('/view', ViewHandler)],
    debug=True)

