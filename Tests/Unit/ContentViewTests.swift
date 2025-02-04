import XCTest
@testable import ScalerApp

final class ContentViewTests: XCTestCase {
    func testCounterInitialValue() {
        let contentView = ContentView()
        XCTAssertEqual(contentView.counter, 0)
    }
} 