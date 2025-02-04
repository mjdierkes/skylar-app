import SwiftUI

struct ContentView: View {
    @State private var counter = 0
    
    var body: some View {
        VStack {
            Text("Counter: \(counter)")
                .accessibilityIdentifier("counterText")
            
            Button("Increment") {
                counter += 1
            }
            .accessibilityIdentifier("incrementButton")
        }
        .padding()
    }
} 