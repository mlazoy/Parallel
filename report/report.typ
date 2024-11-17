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

#let bash_box(file, ..args) = {
  showybox(
    frame: (
      body-color: black,                 // Black background for terminal look
      thickness: 0.6pt
    ),
    breakable: true,
    width: 100%,  // Fill the available width
    align: center,
    color: rgb(0, 255, 0),  // Set default text color to green
  )[
    // Set the text style to green for all code
    #set text(
      font: "DejaVu Sans Mono",   // Monospaced font for terminal look
      size: 0.7em,               // Set text size
      fill: rgb(0, 255, 0)       // Green text color for terminal style
    )
    
    // Read and display the file content
    #sourcefile(
      read(file), 
      file: file, 
      ..args, 
      frame: none,
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

#my_sourcefile("../a1/Game_Of_Life.c")

#pagebreak() 

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

#pagebreak() 

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