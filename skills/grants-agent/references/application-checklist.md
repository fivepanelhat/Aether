# Application HITL checklist

Complete before any portal submit or TPK/MPI send.

## Identity and finance

- [ ] Legal entity name + NZBN verified
- [ ] Authorised signatory named
- [ ] Bank account for reimbursement (secure channel only)
- [ ] 3-year financials / cashflow as required
- [ ] Co-fund source documented and **allowed** by fund rules

## Project truth

- [ ] Technical uncertainty stated (if R&D fund)
- [ ] Milestones map to real repos/releases
- [ ] Hardware BOM matches public target (RPi 5 16GB + Hailo-10H)
- [ ] No "certified SOC 2" claim unless audit complete
- [ ] Version pins accurate against public tags

## Sovereignty and culture

- [ ] Data flow diagram shows local processing boundaries
- [ ] Te Mana Raraunga claims reviewed if Maori data involved
- [ ] Cultural Advisor sign-off if iwi/hapu/whanau/marae named
- [ ] Partner consent letters on file (if joint)

## Compliance

- [ ] Privacy Act purpose limitation stated
- [ ] HITL gates described for high-risk agent actions
- [ ] Incident / breach pathway referenced if handling personal data
- [ ] IPP 3A / biometric code considered when relevant (see repo COMPLIANCE.md)

## Process

- [ ] Grant lead approval
- [ ] Finance approval
- [ ] Tracker status: `hitl_review` then human sets `submitted`
- [ ] Copy of final PDF stored offline with access control

**Agent rule:** Do not tick process boxes on the human's behalf.
