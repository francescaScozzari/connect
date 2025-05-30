context('Homepage', () => {
  describe('Homepage tests', () => {
    beforeEach(() => {
      cy.viewport(1600, 1200)
    })

    it('User can click footer links', () => {
      cy.visit('/')

      cy.contains(/all rights reserved/i)
      cy.get('[data-cy="uda"]').should(
        'have.attr',
        'href',
        'https://en.unich.it/'
      )

      cy.contains(/privacy policy/i)
      cy.get('[data-cy="privacy-policy"]').should(
        'have.attr',
        'href',
        Cypress.env('privacyPolicyUrl')
      )

      cy.contains(/ingenium university/i)
      cy.get('[data-cy="ingenium"]').should(
        'have.attr',
        'href',
        'https://ingenium-eu.education/'
      )

      cy.contains(/bi4e/i)
      cy.get('[data-cy="bi4e"]').should(
        'have.attr',
        'href',
        'https://boosting-ingenium.com/'
      )
    })
  })
})
