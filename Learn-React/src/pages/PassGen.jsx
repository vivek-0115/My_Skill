import React from 'react'
import { useState, useCallback, useEffect, useRef } from 'react'

export default function PassGen() {

  const [lenght, setLength] = useState(8)
  const [isNum, setIsNum] = useState(false)
  const [isChar, setIsChar] = useState(true)
  const [password, setPassword] = useState("")
  const passRef = useRef(null)

  const passwordGenerator = useCallback(() => {

    let pass = ""
    let str = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'

    if (isNum) str += "0123456789"
    if (isChar) str += "!@#$%^&*()_-+={}][:;.<>|`~"

    for (let i = 1; i <= lenght; i++) {
      let char = Math.floor(Math.random() * str.length + 1)
      pass += str.charAt(char)
    }

    setPassword(pass)

  }, [lenght, isNum, isChar])

  useEffect(() => {
    passwordGenerator()
  }, [lenght, isNum, isChar])

  const copy = useCallback(() => {
    passRef.current?.select();
    window.navigator.clipboard.writeText(password);
  }, [password])


  return (
    <div className='min-h-screen flex items-center justify-center'>
      <main className='max-w-3xl bg-white/20 backdrop-blur-lg rounded-2xl shadow-lg p-4'>
      
        <h1 className='text-4xl text-center font-bold text-gray-800 mb-4'>Password Generator</h1>

        <section>

          <div>
            <input type="text" name="password" id="password" className='border outline-0 min-w-sm h-10 p-2 rounded-l-sm'
              value={password}
              ref={passRef}
            />
            <button className='bg-red-300 border border-l-0 px-4 h-10 rounded-r-sm cursor-pointer'
              onClick={() => { copy() }}
            >
              Copy
            </button>
          </div>

          <section className='flex justify-around mt-4'>

            <div className='flex items-center gap-2'>
              <input type="range" name="length" id="length"
                value={lenght} min={8} max={32}
                onChange={(e) => { setLength(e.target.value) }}
              />
              <label htmlFor="length">Length({lenght})</label>
            </div>

            <div className='flex items-center gap-2'>
              <input type="checkbox" name="number" id="number"
                defaultChecked={isNum}
                onChange={() => { setIsNum((prev) => !prev) }}
              />
              <label htmlFor="number">Number</label>
            </div>

            <div className='flex items-center gap-2'>
              <input type="checkbox" name="character" id="character"
                defaultChecked={isChar}
                onChange={() => { setIsChar((prev) => !prev) }}
              />
              <label htmlFor="character">Character</label>
            </div>

          </section>

        </section>
      </main>
    </div>
  )
}
