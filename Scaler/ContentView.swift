import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {
            Image(systemName: "chart.line.uptrend.xyaxis")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("Welcome to Scaler")
        }
        .padding()
    }
}

#Preview {
    ContentView()
} 