#import "./template.typ":report
#import "@preview/codelst:2.0.2": sourcecode, sourcefile, codelst
#import "@preview/showybox:2.0.3": showybox

#show: report.with(
  title: "Συστήματα Παράλληλης Επεξεργασίας",
  subtitle: "Εργαστηριακή Αναφορά",
  authors: ("Λάζου Μαρία-Αργυρώ (el20129)",
            "Σπηλιώτης Αθανάσιος (el20175)"),
  team : "parlab09",
  semester: "9ο Εξάμηνο, 2024-2025",
)

#let my_sourcefile(file, lang: auto, ..args) = {
  showybox(
    frame: (
      body-color: rgb(245, 245, 245), // Light background (like VSCode light theme)
      border-color: rgb(200, 200, 200), // Light gray border
      title-color: rgb(200, 200, 200), // Darker gray title for contrast
      radius: 5pt, // Rounded corners
      thickness: 1pt, // Thin border for a clean look
    ),
    breakable: true,
    width: 100%, // Fill the available width
    align: center,
    color: rgb(80, 80, 80), // Dark gray text (like VSCode)
    title: grid(
      columns: (1fr, 1fr), // Two equal-width columns for title and language
      gutter: 1em, // Space between columns
      text(
        font: "DejaVu Sans Mono", // Monospaced font for code
        size: 0.75em,
        fill: rgb(80, 80, 80), // Dark gray title text
        weight: 600,
        file.split("/").at(-1)
      )
    ),
  )[
    #set text(size: 0.85em, font: "DejaVu Sans Mono", fill: rgb(10, 10, 10)) // Black text for the code
    #sourcefile(read(file), file: file, lang: lang, ..args, frame: none)
  ]
}

#let bash_box(file, lang: auto, ..args) = {
  show table.cell.where(y: 0): set text(weight: "regular")

  showybox(
    frame: (
      body-color: rgb("#111"),
      thickness: 0.6pt,
    ),
    breakable: false,
    width: 100%,
    align: center,
  )[
    #set text(
      font: "DejaVu Sans Mono",
      size: 0.8em,
      fill: lime, // Green text color for terminal style
    )
    #sourcefile(
      read(file),
      file: file,
      // lang: "bash",
      ..args,
      frame: none,
      numbering: none,
    )
  ]
}

#let bordered_text(file) = {
  // Read the file content
  let file_content = read(file)
  
  // Display the file content inside the box
  showybox(
    frame: (
      border-color: black,         
      border-thickness: 1pt,       
      radius: 4pt,                 
      thickness: 1pt,             
    ),
    breakable: true,
    width: 100%,                  
    align: center,
 
    text(size: 12pt, fill: black)[#file_content]  
    )
}

/****************************
* Document body, start here.*
*****************************/

= Conway's GameofLife
\
 === Υλοποίηση
Για την παραλληλοποίηση του αλγορίθμου τροποποίησαμε τον κώδικα που δίνεται προσθέτοντας απλώς το \#pragma directive στο κύριο loop για τα (i,j) του body: 

#my_sourcefile("../a1/Game_Of_Life.c",
highlighted: (63),
  highlight-color: green.lighten(60%))
\

Για την μεταγλώτιση και εκτέλεση στον scirouter χρησιμοποίησαμε το ακόλουθα scripts :

#bash_box("../a1/make_on_queue.sh")
#bash_box("../a1/omp_run_on_queue.sh")
\
=== Aποτελέσματα Μετρήσεων:
\
#bordered_text("../a1/omp_gameoflife_all.out")
\

=== Γραφική Απεικόνιση και Παρατηρήσεις

#image("../a1/grid64.svg")
Παρατηρούμε ότι για μικρό μέγεθος grid (με συνολική απαίτηση μνήμης 4*64*64bytes =
16KB), δεν υπάρχει ομοιόμορφη κλιμάκωση της επίδοσης με αύξηση των νημάτων από 4
και πάνω. Bottleneck κόστους θα θεωρήσουμε την ανάγκη συγχρονισμού των threads και
το overhead της δημιουργίας τους συγκριτικά με τον φόρτο εργασίας που τους ανατίθεται
(granularity).
\
\
\
#image("../a1/grid1024.svg")
Για μέγεθος grid με συνολική απαίτηση μνήμης 4*1024*1024 bytes = 4ΜB, η επίδοση
βελτίωνεται ομοιόμορφα και ανάλογα με το μέγεθος των νημάτων . Εικάζουμε, λοιπόν, πως
η cache χωράει ολόκληρο το grid ώστε το κάθε νήμα δεν επιβαρύνει την μνήμη με loads
των αντίστοιχων rows, o φόρτος εργασίας είναι ισομοιρασμένος στους workers και το
κόστος επικοινωνίας αμελητέο. Συνεπώς, προκύπτει perfect scaling.

#pagebreak() 

#image("../a1/grid4096.svg")
Για μεγάλο grid (με συνολική απαίτηση μνήμης 4*4096*4096 bytes = 64ΜΒ), η κλιμάκωση
παύει να υφίσταται για περισσότερα από 4 νήματα. Bottleneck κόστους εδώ θεωρούμε το
memory bandwidth. Επειδή ολόκληρο το grid δεν χωράει στην cache, δημιουργούνται
misses όταν ξεχωριστά νήματα προσπαθούν να διαβάσουν ξεχωριστές γραμμές του
previous. Σε κάθε memory request αδειάζουν χρήσιμα data για άλλα νήματα, φέρνοντας τις
δικές τους γραμμές και στο μεταξύ oι υπολογισμοί stall-άρουν.


#pagebreak() 

 === Bonus 

Δύο ενδιαφέρουσες ειδικές αρχικοποιήσεις του ταμπλό είναι το pulse και το gosper glider
gun για τις οποίες η εξέλιξη των γενιών σε μορφή
κινούμενης εικόνας φαίνεται με μορφή gif παρακάτω: 

#align(center)[
#image("../a1/glider_gun.gif", width:75%)
#emph("glider_gun animation")
\
\
#image("../a1/pulse.gif", width: 75%)
#emph("pulse animation")
]

#pagebreak() 

=== Πράρτημα

Για την εξαγωγή των γραφικών παραστάσεων χρησιμοποιήθηκε ο κώδικας σε Python που ακολουθεί:

#my_sourcefile("../a1/plots.py")

#pagebreak() 

= KMEANS
\
== 1) Shared Clusters
=== Υλοποίηση
Για την παραλληλοποίηση της συγκεκριμένης έκδοσης χρησιμοπιήσαμε το parallel for directive του οmp και για την αποφυγή race conditions τα omp atomic directives. Αυτά εμφανίζονται όταν περισσότερα από 1 νήματα προσπαθούν να ανανεώσουν τιμές στους shared πίνακες newClusters και newClusterSize σε indexes τα οποία δεν είναι μοναδικά για το καθένα καθώς και στην shared μεταβλητή delta. Για αυτήν προσφέρεται η χρήση reduction και εδώ μπορεί να αγνοηθεί εντελώς αφού η σύγκλιση του αλγορίθμου καθορίζεται από των πολύ μικρό αριθμό των επαναλήψεων(10). Ωστόσω, χρησιμοποιούμε atomic για ορθότητα της τιμής του και για παρατήρηση με βάση το μεγαλύετρο δυνατό overhead.

#my_sourcefile("../a2/kmeans/omp_naive_kmeans.c",
highlighted: (89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114),
  highlight-color: green.lighten(60%)) 
\
Απεικονίζουμε παρακάτω τα αποτελέσματα των δοκιμών στον sandman για τις διάφορες τιμές της environmental variable OMP_NUM_THREADS:
\
#image("../a2/kmeans/results/fig0.png")

Παρατηρούμε πως ο αλγόριθμος δεν κλιμακώνει καθόλου καλά από 8 και πάνω νήματα εξαιτείας της σειριποίησης των εγγραφών ολοένα και περισσότερων νημάτων που επιβάλλει η omp atomic, και της αυξανόμενης συμφόρησης στο bus κατά την απόκτηση του lock.

#pagebreak() 

=== Εκμετάλλευση του GOMP_CPU_AFFINITY 
\

Με την χρήση του environmental variable GOMP_CPU_AFFINITY και στατικό shceduling κάνουμε pin νήματα σε πυρήνες(εφόσον δεν υπάρχει ανάγκη για περίπλοκη δυναμική δρομολόγηση). Έτσι, δεν σπαταλάται καθόλου χρόνος σε flash πυρήνων και αχρείαστη μεταφορά δεδομένων από πυρήνα σε άλλον. 
\
Για την υλοποίηση τροποποίησαμε κατάλληλα το script υποβολής στον sandman και προσθέσαμε την παράμετρο schedule static στο parallel for. Tα αποτελέσματα παρουσιάζονται παρακάτω:
\
#image("../a2/kmeans/results/fig1.png")

Παρατηρούμε σημαντική βελτίωση στην κλιμάκωση μέχρι 8 νήματα όμως μετά σταματάει να κλιμακώνει ο αλγόριθμος λόγω της δομής που έχει ο sandman. Για 16 νήματα και πάνω δεν μπορούμε να τα κάνουμε pin στο ίδιο cluster οπότε δεν μοιράζονται τα νήματα την ίδια L3 cache και υπάρχει συνεχής μεταφορά δεδομένων των shared πινάκων και bus invalidations λόγω του cache coherence protocol. Aκόμη τα L3 misses κοστίζουν ξεχωριστά για κάθε cluster. Εαν αξιοποιήσουμε τo hyperthreading και κάνουμε pin τα threads 9-16 στους cores 32-40 που πέφτουν μέσα στο cluster 1 μπορούμε να μειώσουμε σημαντικά τον χρόνο για τα 16 νήματα. Από εκεί και πέρα η κλιμάκβση σταματάει. Παραθέτουμε την βελτιωμένη εκδοχή των 16 νημάτων ακολούθως:
\

#image("../a2/kmeans/results/fig7.png")

#pagebreak() 

== 2) Copied Clusters & Reduce

=== Yλοποίηση
Μοιράζουμε σε κάθε νήμα ένα διαφορετικό τμήμα των πινάκων newClusters, newClusterSize οπότε τα δεδομένα γίνονται private, δεν υπάρχουν race conditions αλλά απαιτείται reduction (με πρόσθεση) στο τέλος για το τελικό αποτέλεσμα (η οποία πραγματοποιείται εδώ από 1 νήμα). 

// TODO add code here !

=== Aποτελέσματα
#image("../a2/kmeans/results/fig2.png")

Παρατηρούμε τέλεια κλιμάκωση μέχρι και τα 32 νήματα και αρκετά καλή και στα 64 εφόσον δεν εισάγουμε overheads συγχρονισμού και η σειριακή ενοποίηση (reduction) δεν είναι computational intensive για να καθυστρεί τον αλγόριθμο. 
\
\
=== Δοκιμές με μικρότερο dataset

Τα αποτελέσματα δεν είναι ίδια για άλλα μεγέθη πινάκων. Συγκεκριμένα για το επόμενο configuration παρατηρούμε τα εξής:

 #image("../a2/kmeans/results/fig3.png") 

Κυριαρχo ρόλο για αυτην την συμπεριφορά αποτελεί το φαινόμενο false sharing, που εμφανίζεται σε μικρά datasets (εδώ κάθε object έχει μόνο 1 συντεταγμένη!) όταν σε ένα cache line καταφέρνουν να χωρέσουν παραπάνω από 1 objects και σε κάθε εγγραφή γίνονται πάρα πολλά περιττά invalidations. Mια λύση είναι το padding όμως έχει memory overhead και δεν προτιμάται.

=== First-touch Policy 
Προς αποφυγή των παραπάνω εκμεταλλευόμαστε την πολιτική των linux κατά το mapping των virtual με physical addresses. H δέσευση φυσικής μνήμης πραγματοποιείται κατά την 1η εγγραφή του αντικειμένου (η calloc το εξασφαλίζει γράφοντας 0 ενώ η malloc όχι) οπότε εαν το κάθε νήμα γράψει ξεχωριστά στο κομμάτι του πίνακα που του αντιστοιχεί (ουσιαστικά παραλληλοποιώντας την αντιγραφή των shared πινάκων) θα απεικονιστεί στην μνήμη του αυτό και μόνο. 
=== Υλοποίηση 
// TODO add code here !
#my_sourcefile("../a2/kmeans/omp_reduction_kmeans.c")

=== Αποτελέσματα 

#image("../a2/kmeans/results/fig4.png")

Υπάρχει σαφής βελτίωση και καλή κλιμάκωση μέχρι τα 32 νήματα ακόμα και σε σχέση με την ιδανική εκτέλεση του σειριακού αλγορίθμου. Ο καλύτερος χρόνος σε αυτό το ερώτημα είναι 0.4605s στα 32 νήματα! 

=== Numa-aware initialization

Με βάση όσα αναφέρθηκαν για το pinning σε cores και την πολιτική first-touch η αρχικοποίηση των shared πινάκων μπορεί να γίνει και αυτή ατομικά από κάθε νήμα σε ένα private τμήμα αυτού. Για την υλοποίηση προσθέτουμε το omp parallel for directive με στατική δρομολόγηση. Aυτή είναι απαραίτητη ώστε τα νήματα που θα βάλουν τους τυχαίους αριθμούς στα objects να είναι τα ίδια νήματα με αυτά που θα τα επεξεργαστούν στην main.c με σκοπό να είναι ήδη στις caches και να μην χρειάζεται να τα μεταφέρνουν από την κύρια μνήμη ή από άλλα νήματα. 
=== Υλοποίηση 
Τροποποιούμε το file_io.c που δίνεται : 
// TODO add code here !
#my_sourcefile("../a2/kmeans/file_io.c",
highlighted: (28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50),
  highlight-color: green.lighten(60%),
)



\
=== Αποτελέσματα 

#image("../a2/kmeans/results/fig5.png")

Παρατηρούμε καλύτερη κλιμάκωση μέχρι τα 32 νήματα με χρόνο 0.2667s!
Το κυρίαρχο bottleneck σε αυτήν την περίπτωση είναι το overhead της δημιουργίας των νημάτων.

\
\
Tέλος με όλες τις προηγούμενες αλλαγές δοκιμάζουμε ξανά το μεγάλο dataset που είχαμε στην αρχή:

#image("../a2/kmeans/results/fig6.png")

Παρατηρούμε πως υπάρχει τέλεια κλιμάκωση του αλγορίθμου. Οπότε bottleneck θα μπορούσε να θεωρηθεί το computive intensity για κάθε object.

#pagebreak() 

= FLOYD WARSHALL

== 1) Recursive 

=== Υλοποίηση

\
Δημιουργούμε ένα παράλληλο section κατά την πρώτη κλήση αφού έχουμε ενεργοποιήσει την επιλογή για nested tasks μέσω τηw  omp_set_nested(1). (*Μπορούμε να το θέσουμε και ως environmental variable (OMP_NESTED=TRUE)*)
Για την διατήρηση των εξαρτήσεων κατά τον υπολογισμό των blocks (A11) -> (A12 A21) -> A22 και αντιστρόφως τοποθετούμε κατάλληλα barriers έμμεσα με τα taskwait directives. 

#my_sourcefile("../a2/FW/fw_sr.c",
highlighted: (13,43,47,48,49,50,51,52,53,93,95,97,100,102,104),
  highlight-color: green.lighten(60%))

\
Πειραματιστήκαμε σχετικά με την βέλτιστη τιμή του BSIZE τρέχοντας τις προσομοιώσεις που ακολουθούν. Διαισθητικά η optimal τιμή οφείλει να εκμεταλλεύεται πλήρως το cache size και δεδομένου ότι έχουμε τετράγωνο grid για 1 recursive call που δημιουργεί 4 sub-blocks μεγέθους B θα είναι Βopt = sqrt(cache size).

== Aποτελέσματα 
\
#align(center)[
===  {N = 1024}
#image("../a2/FW/results/fig1024_16.png", width:60%)
#image("../a2/FW/results/fig1024_32.png", width:60%)
#image("../a2/FW/results/fig1024_64.png", width:60%)
#image("../a2/FW/results/fig1024_128.png", width:60%)
#image("../a2/FW/results/fig1024_256.png", width:60%)

=== {N = 2048}
#image("../a2/FW/results/fig2048_16.png", width:60%)
#image("../a2/FW/results/fig2048_32.png", width:60%)
#image("../a2/FW/results/fig2048_64.png", width:60%)
#image("../a2/FW/results/fig2048_128.png", width:60%)
#image("../a2/FW/results/fig2048_256.png", width:60%)

=== { N = 4096 }
#image("../a2/FW/results/fig4096_16.png", width:60%)
#image("../a2/FW/results/fig4096_32.png", width:60%)
#image("../a2/FW/results/fig4096_64.png", width:60%)
#image("../a2/FW/results/fig4096_128.png", width:60%)
#image("../a2/FW/results/fig4096_256.png", width:60%)
]

Kαταλήξαμε πως η ιδανική τιμή είναι Β=64 και ο καλύτερος χρόνος που πετύχαμε χρησιμοποιώντας αυτήν για 4096 μέγεθος πίνακα ήταν 10.4486 με 16 threads. Από το σημείο αυτό και έπειτα ο αλγόριθμος δεν κλιμακώνει και φανερώνει την αδυναμία του χάρη στην αναδρομή.

#pagebreak() 

== 2) TILED

=== Υλοποίηση 

Φτιάχνουμε 1 παράλληλo section με κατάλληλα barriers ώστε να υπλογίζεται πρώτα (single) το k-οστό στοιχείο στην διαγώνιο, έπειτα όσα βρίσκονται κατά μήκος του "σταυρού" που σχηματίζεται εκατέρωθεν αυτού, και τέλος τα blocks στοιχείων που απομένουν. Καθένα από τα στάδια 2 και 3 έχει 4 for loops που μπορούν να παραλληλοποιηθούν με parallel for και επειδή είναι ανεξάρτητα μεταξύ τους με παράμετρο nowait. Το collapse(2) πραγματοποιεί flattening για καλύτερη λειτουργία του parallel for για nested loops. Mε χρήση μόνο των παραπάνω επιτυγχάνουμε χρόνο εκτέλεσης 2.2 secs.  
\
Για περαιτέρω βελτίωση επιχειρήσαμε να χρησιμοποιήσουμε SIMD εντολές αρχικά μέσω του OpenMP με το αντίστοιχο directive και στην συνέχεια γράφοντας χειροκίνητα τις intrinsics εντολές για AVX μοντέλο που υποστηρίζει 4-size vector operations καθώς διαπιστώσαμε ότι vector operations μεγαλύτερου μεγέθους (π.χ με 8 στοιχεία AVX2) δεν υποστηρίζεται στο εν λόγω μηχάνημα και λαμβάνουμε σφάλμα Illegal hardware instruction. Στην πρώτη εκδοχή λάβαμε συνολικό χρόνο εκτέλεσης 1.7secs. 
\
H χρήση των intrisincs απευθείας μας δίνει την δυνατότητα να εκμεταλλευτούμε πλήρως και την αρχιτεκτονική της κρυφής μνήμης μέσω loop unrolling. Συγκεκριμένα, αναγνωρίσαμε ότι το size του cacheline είναι 64bytes, συνεπώς χωράνε 16 integers, ή 4 vectors 4άδων σε όρους AVX. Άρα επιτυγχάνουμε μέγιστο locality exploitation κάνοντας unroll με παράγοντα 4 και αυξάνοντας το j κατά 16 σε κάθε iteration. Ακόμη, παρατηρούμε ότι τα στοιχεία Α[i][k] είναι ανεξάρτητα του j  και η φόρτωση αυτών των vectors μπορεί να γίνει στο εξωτερικό loop. O καλύτερος χρόνος εκτέλεσης που επιτύχαμεμε αυτήν την εκδοχή είναι *1.39 secs!*
\

#my_sourcefile("../a2/FW/fw_smd.c")

=== Aποτελέσματα 

#image("../a2/FW/results/tiled.png")

Βλέπουμε πως υπάρχει τέλεια κλιμάκωση με αύξηση των threads. 


#pagebreak() 

== Παράρτημα 
\
Για την δημιουργία των γραφικών παραστάσεων χρημιοποίηθηκε oι εξής κώδικες σε Python :

#my_sourcefile("../a2/kmeans/results/results.py")
\
\
#my_sourcefile("../a2/FW/results/plots.py")



