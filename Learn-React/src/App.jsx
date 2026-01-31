import { useState } from 'react'

function App() {

  let [counter, setCounter] = useState(0)

  const Increment = () => {
    setCounter(counter+1)
  }

  const Decrement = () => {
    setCounter(counter-1)
  }

  return (
    <>
      <h1>BytesCode | Vivek Kumar</h1>
      <h3>Counter Value: {counter}</h3>
      <button onClick={Increment}>Increment</button>
      <button onClick={Decrement}>Decrement</button>
    </>
  )
}

export default App
