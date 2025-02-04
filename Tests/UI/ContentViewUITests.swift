import XCTest

final class ContentViewUITests: XCTestCase {
    func testCounterIncrement() throws {
        let app = XCUIApplication()
        app.launch()
        
        let counterText = app.staticTexts["counterText"]
        XCTAssertEqual(counterText.label, "Counter: 0")
        
        let incrementButton = app.buttons["incrementButton"]
        incrementButton.tap()
        
        XCTAssertEqual(counterText.label, "Counter: 1")
    }
} 