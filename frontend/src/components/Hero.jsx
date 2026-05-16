import { motion } from 'framer-motion'
import { text } from '../content/text'
import HeroDemoAnimation from './HeroDemoAnimation'
import '../Herodemo.css'

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6, ease: 'easeOut', delay }
})

function Hero({ lang }) {
  const t = text[lang]

  return (
    <section className="hero hero-split">
      <div className="hero-bg">
        <HeroDemoAnimation />
      </div>
      <div className="hero-glow" />
      <div className="hero-content">
        <motion.div {...fadeUp(0.1)}>
          <div className="hero-tag">
            <span className="hero-tag-dot" />
            <span>{t.heroTag}</span>
          </div>
        </motion.div>

        <motion.h1 className="hero-title" {...fadeUp(0.2)}>
          <span className="hero-title-main">{t.heroH1Part1}</span>
          <span className="hero-title-accent">{t.heroH1Em}</span>
        </motion.h1>

        <motion.p className="hero-sub" {...fadeUp(0.3)}>
          {t.heroSub}
        </motion.p>
      </div>
    </section>
  )
}

export default Hero
